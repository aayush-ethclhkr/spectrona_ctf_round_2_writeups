"""Decode the JSON payload of a three-part JWT without verifying its signature."""

import base64
import json
import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: py decode_jwt.py <file-containing-JWT>")

    token = Path(sys.argv[1]).read_text(encoding="utf-8").strip()
    parts = token.split(".")
    if len(parts) != 3:
        raise SystemExit(f"Expected a 3-part JWT; found {len(parts)} part(s)")

    payload = parts[1]
    payload += "=" * (-len(payload) % 4)
    data = json.loads(base64.urlsafe_b64decode(payload).decode("utf-8"))
    print(json.dumps(data, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
