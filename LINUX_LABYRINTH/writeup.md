# SPECTRONA — Linux Labyrinth

**Category:** Linux / Forensics  
**Challenge:** Linux Labyrinth  
**Archive:** `linux-labyrinth-player.tar.gz`  
**Flag:** `SPECTRONA{linux_is_all_about_knowing_commands}`

## Overview

This challenge is a guided Linux command-line investigation. Its opening clue says to look for entries by metadata rather than by filename. Following the trail uses file permissions, inode and link metadata, symlinks, log counting, nested archives, strings in a binary, sparse-file allocation, and byte counts. The archive is evidence: inspect it with standard tools; do not execute its files or unpack every nested archive blindly.

The steps below use a Linux shell. They avoid Python, Perl, Ruby, Node, and interactive editors, as required by the challenge.

## 1. Extract the challenge archive

Copy the archive to a Linux machine (or Kali VM), then extract it while preserving the archive’s file metadata and links:

```bash
mkdir -p ~/linux-labyrinth
tar -xzpf linux-labyrinth-player.tar.gz -C ~/linux-labyrinth
cd ~/linux-labyrinth/linux-labyrinth
find . -maxdepth 2 -type f -print
```

The extracted tree is under `evidence/`.

## 2. Start with metadata

List permissions, sizes, link counts, and paths. This makes the unusual entries visible without relying on their names:

```bash
find evidence -type f -printf '%m %s bytes links=%n %p\n' | sort
```

The owner-only files have mode `600`. Inspect those candidates, using `--` so a leading dash in a filename is treated as a path rather than an option:

```bash
find evidence -type f -perm 0600 -print
cat -- evidence/01_noise/owner_read.txt
```

`owner_read.txt` is a decoy. Keep following the other metadata clues rather than assuming that the first matching file is the answer.

## 3. Find the shared inode and follow the symlinks

Search for files with multiple hard links and compare their inode numbers:

```bash
find evidence -type f -links +1 -exec ls -li {} +
stat -c 'inode=%i links=%h path=%n' evidence/02_inodes/orbit.log evidence/02_inodes/backup/orbit.copy
cat evidence/02_inodes/orbit.log
```

`orbit.log` and `backup/orbit.copy` share an inode. The content directs you to inspect the gateway. The symlink chain resolves to the hidden `-cipher_note` file:

```bash
readlink evidence/03_links/alias
readlink evidence/03_links/gateway
readlink -f evidence/03_links/alias
cat -- evidence/03_links/alias
```

The note is Base64 encoded. Decode it directly:

```bash
base64 -d < evidence/04_permissions/-cipher_note
```

It says to find the client that appears exactly once in the log, count first, then take that request’s path.

## 4. Count log clients before extracting the request path

Count occurrences of each client address:

```bash
awk '{print $1}' evidence/05_logs/access.log | sort | uniq -c | sort -n
```

There are two one-off addresses, including a decoy. Inspect the corresponding records and select the analyst’s successful request:

```bash
awk '$1 == "172.19.77.241"' evidence/05_logs/access.log
awk '$1 == "172.19.77.241" {print $7}' evidence/05_logs/access.log
```

The useful request path is `/ledger/fragment-3`. It points onward to the archive/fragment portion of the evidence; it is not itself the flag.

## 5. Read the nested archives as a stream

The archive clue says to use `tar` as a stream and not blindly unpack everything. First inspect the outer archive’s member list, then extract only the embedded archive:

```bash
tar -tzf evidence/06_archives/outer.tar.gz
tar -xOzf evidence/06_archives/outer.tar.gz a/middle.tar.bz2 > /tmp/middle.tar.bz2
tar -tjf /tmp/middle.tar.bz2
```

Extract only the next nested archive, then list its member:

```bash
tar -xOjf /tmp/middle.tar.bz2 a/b/c/final-note.txt.xz > /tmp/final-note.txt.xz
7z x -so /tmp/final-note.txt.xz
```

The note says to use `xxd` next.

## 6. Inspect the binary strings

The readme in the binary directory points to the other file. Use `strings`; do not run the binary:

```bash
cat evidence/07_binary/readme.bin
strings -a evidence/07_binary/blob.bin
```

The output instructs you to compare `du` and `stat` on `memory.img`, which is a sparse file, and inspect its allocated tail.

## 7. Locate the allocated tail of the sparse file

Compare its logical size with its allocated disk usage:

```bash
stat -c 'logical size: %s bytes; allocated blocks: %b (block size: %B bytes)' evidence/08_sparse/memory.img
du -h evidence/08_sparse/memory.img
```

The logical size is 33,554,432 bytes, but most of the file is a hole. In the supplied image, the allocated data extent containing the clue begins at byte offset `33546240` (`0x1ff0000`) and is 8,192 bytes long. Read just that extent and inspect its printable strings:

```bash
dd if=evidence/08_sparse/memory.img bs=1 skip=33546240 count=8192 status=none | strings -a
```

The tail says there are seven shards and their order is encoded by byte length; NUL padding is not part of the flag. Do not use the logical end-of-file decoy as a shard.

## 8. Order the shards by byte length and assemble the flag

Use `wc -c` to show the shard sizes. The named shards are `01_header` through `07_tail`; the `x_decoy` and `y_decoy` files are not part of the seven-piece set.

```bash
for f in evidence/09_fragments/{01_header,02_word,03_word,04_word,05_word,06_word,07_tail}; do
  printf '%s\t%s\n' "$(wc -c < "$f")" "$f"
done | sort -n
```

The sizes run from 10 through 16 bytes and therefore give the order. Each later piece is NUL-padded. Remove those padding bytes while concatenating:

```bash
for f in evidence/09_fragments/{01_header,02_word,03_word,04_word,05_word,06_word,07_tail}; do
  tr -d '\000' < "$f"
done
printf '\n'
```

The pieces form:

```text
SPECTRONA{linux_is_all_about_knowing_commands}
```

## Command trail summary

```text
find/stat       - discover permissions, inode counts, and link relationships
readlink/cat    - follow the symlink route to the encoded note
awk/sort/uniq   - count log clients, then extract the valid request path
tar/7z          - stream through the nested archives
strings/xxd     - inspect printable clues in binary evidence
du/stat/dd      - locate and read the sparse file's allocated tail
wc/sort/tr      - order the seven fragments and remove NUL padding
```

## Final flag

```text
SPECTRONA{linux_is_all_about_knowing_commands}
```
