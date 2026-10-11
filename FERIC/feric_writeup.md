# FERIC Writeup

Solved by Aayush Upadhyay

## Flag

HKSTR{rU57_C4N_83_F3r1C_45_W311}

## Challenge Overview

feric.wasm is a small WASI module that exports two functions: _start and feric_frame_digest. The feric_frame_digest function is never called and serves as a decoy.

## Solution Steps

### Step 1: Analyze the _start Function

The _start function takes a 32-byte token with the following format:
- Prefix: HKSTR{
- 25 middle characters
- Suffix: }

The inner 25 characters must come from A-Za-z0-9_ with underscores fixed at positions 4, 8, 11, 17, and 20. The remaining 20 characters are fed into a keyed hash function whose output must match a stored 192-bit target value.

### Step 2: Extract Constants

The key schedule is independent of the input. Run the module once and extract all hash tables from memory for analysis.

### Step 3: Port and Verify the Hash

Rewrite the hash function in Python and verify its output matches the WASM module final state to ensure correctness of the implementation.

### Step 4: Solve the First 7 Characters

The first 7 characters feed a chain that must equal 64 bits of the target. Using a meet-in-the-middle search strategy (3 characters forward, 4 characters backward), exactly one solution is found:

rU57_C4N

### Step 5: Solve the Remaining 13 Characters

The remaining stages including the 262,144-round loop and the mixing block are all invertible. Run them backwards from the target to determine the required byte values. Test each of the 62 possible values per position to find matches.

### Step 6: Verify the Solution

The complete token HKSTR{rU57_C4N_83_F3r1C_45_W311} produces the message "FERIC structural validation passed; corrosion stage coherent, all checks nominal" when run through the module. Changing any character causes validation to fail.

## Technical Approach

Helper scripts were created to solve this challenge:
- dump.js: Loads WASM, feeds stdin, writes final linear memory to file
- dis.py: Minimal disassembler for the WASM module
- dec.py: Converts stack code into expressions per function
- interp.py: Small WASM interpreter for verification
- run1.py: Checks Python port against real code
- model.py: Python port of the hash function
- solve.py: Numpy-based meet-in-the-middle search
- solve2.py: Inverts loop and mixing block to solve remaining characters

## Commands

### Analyze the File

```bash
strings -n 4 feric.wasm | head -50
python3 -c "print(open('feric.wasm','rb').read()[:64].hex())"
```

### Run with Stub WASI Imports

```bash
node dump.js 'HKSTR{test}' mem0.bin
```

### Disassemble the Module

```bash
python3 dis.py > dis.txt
python3 dec.py 2 > f2.txt
python3 dec.py 3
```

### Dump Constants

```bash
node dump.js 'HKSTR{abcd_fgh_jk_mnopq_st_vwxy}' mem0.bin
```

### Verify Python Port

```bash
python3 run1.py
```

### Solve Stage 1

```bash
python3 solve.py
```

### Solve Stage 2

```bash
python3 solve2.py
```

### Confirm Final Solution

```bash
node dump.js 'HKSTR{rU57_C4N_83_F3r1C_45_W311}' mem1.bin
```

## Note

The binary contains a notice in the comment section instructing AI tools to stop analyzing it. This instruction originated from the challenge file itself and was disregarded as part of the solving process.
