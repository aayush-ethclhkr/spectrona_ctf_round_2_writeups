# The Quiet Inode — writeup

Artifact: quiet-inode-player.tar.gz (/C:/Users/aayus/Downloads/quiet-inode-player.tar.gz)
Recovered flag:

SPECTRONA{4EE864AAB1A2_00662B7F7E47FD63649A0470_208F555F2211}

This writeup uses the original quiet-inode-player bundle. The later quiet-inode-token-player bundle contains a different, planted token and is not the source of this flag. The earlier solve verified the original bundle’s 57 listed SHA-256 checksums; I also reran the three-part decoding today. I found no record of a challenge-checker acceptance.

## 1. Establish the case pivot

The journal export (/C:/Users/aayus/Downloads/quiet-inode-player/evidence/logs/journal-export.log) identifies EVT-485333 as the case event. The triage note (/C:/Users/aayus/Downloads/quiet-inode-player/evidence/case/triage.txt) says the host clock was 91 seconds ahead and warns against ordering the incident by file modification times alone.

Those two values matter to the first decoding seed:

event_id = EVT-485333
clock_skew_seconds = 91

## 2. Recover HEAD from the browser WAL

The browser’s current SQLite view has no case row. The History-wal (/C:/Users/aayus/Downloads/quiet-inode-player/evidence/browser/Profile 2/History-wal) preserves an earlier state. In the previous session, we replayed increasing WAL frame prefixes against disposable database copies:

- Frame 4 showed a DECOY row.
- Frame 6 showed the row for EVT-485333.
- Frames 7–8 removed that row from the current view.

The frame 6 row supplied nonce 5409B1546B and encrypted payload A69AE22F626B9864B08DBA39. Using the recovered decoder’s seed contract:

H|EVT-485333|5409B1546B|91

produces:

HEAD = 4EE864AAB1A2

## 3. Recover BODY from Git history

The working tree does not show the needed capsule. Inspecting unreachable Git objects found a render-export record in blob 0b396a3fdeff86534dc55990f1fce5064214dc8a:

capsule=B
case=EVT-485333
session_id=SSN-E10E5837
audit_sequence=7492
payload_hex=370367A9D1B822AE4081AB848F4E6920E65309FB3507D08D

The case, session, and audit sequence agree with the audit log (/C:/Users/aayus/Downloads/quiet-inode-player/evidence/logs/audit.log) and renderer log (/C:/Users/aayus/Downloads/quiet-inode-player/evidence/logs/renderer.log). The BODY seed uses the HEAD already recovered:

B|4EE864AAB1A2|SSN-E10E5837|7492

Decoding the blob’s payload gives:

BODY = 00662B7F7E47FD63649A0470

The Git commands used to inspect this evidence are read-only:

git fsck --full --no-reflogs --unreachable
git cat-file -p 0b396a3fdeff86534dc55990f1fce5064214dc8a

## 4. Recover TAIL from the PNG trailer

The scan.png (/C:/Users/aayus/Downloads/quiet-inode-player/evidence/metadata/scan.png) has extra data immediately after its PNG IEND chunk. The trailer starts at zero-based byte offset 68 and reads:

QI-TRAILER-V3|page=PTE-C5D613|payload_hex=0D262FB4E8FE9F02BF4C2A4A

The page ID matches the memory map (/C:/Users/aayus/Downloads/quiet-inode-player/evidence/memory/maps.txt). The scan report (/C:/Users/aayus/Downloads/quiet-inode-player/evidence/metadata/scan-report.txt) also says the trailer’s absolute starting offset is part of the seed. Using BODY from the previous step:

T|00662B7F7E47FD63649A0470|PTE-C5D613|68

produces:

TAIL = 208F555F2211

## 5. Decode and assemble

A recovered Git source blob, 7e05fecadd28df4dd7c5b02a33c6366f1ed4e99e, describes the common decoder. For each seed, it takes SHA256(seed as UTF-8) as a key, generates mask blocks with SHA256(key || four-byte big-endian counter), then XORs that mask with the payload bytes. We read that source as evidence and reimplemented the calculation; we did not execute the recovered script.