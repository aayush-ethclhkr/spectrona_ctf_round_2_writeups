"""Extract bytes packed from the RGB least-significant bits of a PNG."""

import sys

from PIL import Image


def extract_rgb_lsb(path: str) -> bytes:
    image = Image.open(path).convert("RGB")
    # RGB conversion guarantees 3 bytes per pixel, in R/G/B order.
    bits = [channel & 1 for channel in image.tobytes()]

    output = bytearray()
    for offset in range(0, len(bits) - 7, 8):
        value = 0
        for bit in bits[offset:offset + 8]:
            value = (value << 1) | bit
        output.append(value)
    return bytes(output)


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: py extract_lsb.py <image.png>")

    raw = extract_rgb_lsb(sys.argv[1])
    message = raw.split(b"\x00", 1)[0]
    print(message.decode("utf-8", errors="replace"))


if __name__ == "__main__":
    main()
