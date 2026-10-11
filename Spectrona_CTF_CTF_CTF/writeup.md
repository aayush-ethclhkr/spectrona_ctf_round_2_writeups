# Spectrona CTF CTF CTF Writeup

Solved by Aayush Upadhyay

## Flag

SPECTRONA{af2bffdaa2e586c73938542229ee823d57a72493fca828652860b2f0e6ea7ec9}

## Challenge Overview

This challenge spans the Spectrona event site and shared Google Drive folders. A JWT points to a folder of images where RGB least significant bits (LSBs) in two PNGs reveal the next clues. These clues lead to three Blender files containing geometric glyphs that encode three hexadecimal fragments which concatenate to form the final 64-character flag value.

## Prerequisites

```powershell
Get-ChildItem
```

Install Python packages used in the solution:

```powershell
py -m pip install --user pillow
```

Note: The py launcher is Windows Python launcher. If unavailable, replace py with python or python3.

## Solution Steps

### Step 1: Start from the Spectrona CTF Event

Navigate to the Spectrona CTF event page:

https://spectrona.in/events/TEC-03

The event points to this shared Google Drive folder:

https://drive.google.com/drive/folders/1eVPQQmvTlqm3F6ZGwqBZx7BpknAnyjcN

Download the one.txt file which contains a JSON Web Token (JWT).

### Step 2: Decode the JWT Payload

A JWT consists of three dot-separated parts. The second part is Base64URL-encoded JSON. This step decodes the payload to extract the challenge clue. No signing key is needed as the clue is readable in the payload itself.

Create decode_jwt.py:

```python
import base64
import json
import sys
from pathlib import Path

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
```

Run the decoder:

```powershell
py .\decode_jwt.py .\one.txt
```

The payload name value reveals this Google Drive folder:

https://drive.google.com/drive/folders/1i1AS-J8G8S-s9DKWKlU94GAcvBMTMZz4

Open the folder, then navigate to the helloMotto subfolder containing numbered sample images.

### Step 3: Extract RGB LSB Message from sample_07.png

For each pixel, extract the lowest bit of red, green, and blue values in that order. Group the resulting bits into bytes (most-significant bit first), then interpret as text. The extracted text begins with a Google Drive folder URL.

Create extract_lsb.py:

```python
from pathlib import Path
import sys

from PIL import Image


def extract_rgb_lsb(path: str) -> bytes:
    image = Image.open(path).convert("RGB")
    bits = [channel & 1 for channel in image.tobytes()]

    output = bytearray()
    for offset in range(0, len(bits) - 7, 8):
        value = 0
        for bit in bits[offset:offset + 8]:
            value = (value << 1) | bit
        output.append(value)
    return bytes(output)


if len(sys.argv) != 2:
    raise SystemExit("Usage: py extract_lsb.py <image.png>")

raw = extract_rgb_lsb(sys.argv[1])
message = raw.split(b"\x00", 1)[0]
print(message.decode("utf-8", errors="replace"))
```

Run the extraction:

```powershell
py .\extract_lsb.py .\sample_07.png
```

The output reveals:

https://drive.google.com/drive/folders/1Eszh1Z-np1rvRGhfdCFCQY7fzUYzC47N

Download spectrona_part_a.blend from that folder. The accompanying clue states:

"did you know spectrona plays chess?"

### Step 4: Follow the Chess Clue to Part B

The chess clue refers to the Spectrona Chess Competition event:

https://spectrona.in/events/GAM-17

The event rules include this shared folder:

https://drive.google.com/drive/folders/1NzkB4G4rAqh61SIdGRj6uEZicyXXLSNs

Download spectrona_part_b.blend and its PNG reference image from that folder.

### Step 5: Extract and Decode the Second JWT for Part C

Run the LSB extraction script on sample_27.png to extract a complete JWT:

```powershell
py .\extract_lsb.py .\sample_27.png
```

Capture the JWT output to a file and decode it:

```powershell
$jwt = py .\extract_lsb.py .\sample_27.png
Set-Content -LiteralPath .\sample_27.jwt.txt -Value $jwt -NoNewline -Encoding ascii
py .\decode_jwt.py .\sample_27.jwt.txt
```

The JWT payload name claim reveals:

https://drive.google.com/drive/folders/1bQCB1S6dcQe9OxtDh_YSHwDb325fkzeS

Download spectrona_part_c.blend from that folder.

### Step 6: Render the Blender Files

Install Blender and ensure blender.exe is on PATH. Verify installation:

```powershell
blender --version
```

Create render_blend.py to render the currently opened scene to PNG:

```python
import bpy
from pathlib import Path

scene = bpy.context.scene
scene.render.engine = "BLENDER_WORKBENCH"
scene.display.shading.light = "STUDIO"
scene.display.shading.color_type = "MATERIAL"
scene.render.resolution_x = 1400
scene.render.resolution_y = 850
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.render.filepath = str(Path(bpy.data.filepath).with_suffix(".png"))
bpy.ops.render.render(write_still=True)
```

Render each part:

```powershell
blender -b .\spectrona_part_a.blend -P .\render_blend.py
blender -b .\spectrona_part_b.blend -P .\render_blend.py
blender -b .\spectrona_part_c.blend -P .\render_blend.py
```

The -b option runs Blender in background mode and -P executes the Python script. Open the resulting PNG files in an image viewer and read the glyphs left to right across the top row, then left to right across subsequent rows.

### Step 7: Inspect Scene Objects and Verify Glyphs

The scenes use mesh objects named GlyphMesh_*. Create inspect_blend.py to export scene objects, mesh counts, coordinates, and polygons to JSON:

```powershell
blender -b .\spectrona_part_a.blend -P .\inspect_blend.py
blender -b .\spectrona_part_b.blend -P .\inspect_blend.py
blender -b .\spectrona_part_c.blend -P .\inspect_blend.py
```

This generates JSON files for each part. For a compact view of glyph object names and topology counts:

```powershell
@'
import json
from pathlib import Path

for part in "abc":
    data = json.loads(Path(f"spectrona_part_{part}.json").read_text(encoding="utf-8"))
    glyphs = sorted(
        (obj for obj in data["objects"] if obj["name"].startswith("GlyphMesh_")),
        key=lambda obj: obj["name"],
    )
    print(f"Part {part.upper()}: {len(glyphs)} glyph meshes")
    for obj in glyphs:
        print(obj["name"], "vertices", obj["vertices"],
              "edges", obj["edges"], "faces", obj["faces"])
'@ | py -
```

The mesh topology (vertices, edges, faces) provides a signature for matching repeated glyph shapes between scenes. Parts A and C provide clear reference symbols. Matching signatures help confirm ambiguous glyphs in Part B.

### Step 8: Recover and Assemble the Fragments

The three scenes decode to the following fragments:

| Scene | Fragment | Characters |
|-------|----------|------------|
| Part A | af2bffdaa2e586c7393854 | 22 |
| Part B | 2229ee823d57a72493fca | 21 |
| Part C | 828652860b2f0e6ea7ec9 | 21 |

The lengths total 64 hexadecimal characters. Concatenate in order A, B, C:

```powershell
$a = 'af2bffdaa2e586c7393854'
$b = '2229ee823d57a72493fca'
$c = '828652860b2f0e6ea7ec9'
$hex = $a + $b + $c
if ($hex.Length -ne 64) { throw "Expected 64 hex characters; got $($hex.Length)" }
$flag = "SPECTRONA{$hex}"
$flag
Set-Content -LiteralPath .\flag.txt -Value $flag -NoNewline -Encoding utf8
```

Final Flag:

SPECTRONA{af2bffdaa2e586c73938542229ee823d57a72493fca828652860b2f0e6ea7ec9}

## Files Created During Solve

- decode_jwt.py: Decodes JWT payload from text file
- extract_lsb.py: Extracts RGB channel LSBs from image and prints message
- render_blend.py: Renders Blender scene to PNG
- inspect_blend.py: Exports Blender scene and mesh details to JSON
- spectrona_part_a.png, spectrona_part_b_reference.png, spectrona_part_c.png: Scene renders and reference images
- flag.txt: Assembled flag
