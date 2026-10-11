Linux Linux what's this sudden influx by Sudipta.

The correct investigation chain was:

quiet-inode-token-player.tar.gz
        ↓
browser WAL + unreachable Git blob + PNG trailer
        ↓
three Base64URL strings forming a JWT
        ↓
decode the JWT payload
        ↓
"name": "find my github XD"
        ↓
identify challenge creator Sudipta Ranjan Baruah
        ↓
https://github.com/sudiptaranjanbaruah?tab=repositories
        ↓
spectrona_spectrona repository
        ↓
galf.md
        ↓
decode its second JWT

The initial reconstructed JWT was:

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6ImZpbmQgbXkgZ2l0aHViIFhEIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0.Mk4Y2K3K5PYgf2Cd2Y5eSQpmYTyWF-8VYS66DlRZnR0

Its payload decodes to:

{
  "sub": "1234567890",
  "name": "find my github XD",
  "admin": true,
  "iat": 1516239022
}

That JWT was a clue, rather than the final flag. Following it led to Sudipta’s GitHub account and the spectrona_spectrona repository. Its galf.md contains another JWT whose name field decodes to the three-part flag.

For Linux Linux, the recovered value was:

SPECTRONA{4EE864AAB1A2_00662B7F7E47FD63649A0470_208F555F2214}