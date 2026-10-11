# PATINA — Writeup

Challenge: PATINA
Author: cursorhigh / HacksterSec
Category: WebAssembly reverse engineering
Artifact: patina.wasm
Final flag:

HKSTR{rU57_n3v3r_5l33p5}

## 1. Verify the artifact

The supplied module is 3,715 bytes. Its SHA-256 matches the challenge:

7cb6862d75146b2caccf988124a51323fd3fa091dc478c4649b79abf06c513c3

Verified local artifact: patina.wasm (/C:/Users/aayus/Downloads/patina-solve/patina.wasm)

## 2. Convert WebAssembly to readable WAT

The module was converted from WASM into WebAssembly text format. The resulting patina.wat (/C:/Users/aayus/Downloads/patina-solve/patina.wat) made the validation routine easier to follow.

The module imports only three WASI functions:

fd_read
fd_write
proc_exit

Its behavior is simple:

1. Read one input from standard input.
2. Validate its length and wrapper.
3. Transform the 17-byte body.
4. Compare the transformed bytes with an embedded target.
5. Print either accept or reject.

There were no useful symbols or diagnostic messages.

## 3. Determine the required format

The checker expects exactly 24 characters:

HKSTR{<17-byte body>}

The fixed portions use seven characters:

HKSTR{  = 6 bytes
}      = 1 byte

That leaves a body of exactly 17 bytes.

A dummy input with the correct structure was therefore used:

HKSTR{AAAA_AAAAA_AAAAAA}

## 4. Recover the transformation constants

An instrumented copy of the module was used to preserve its working memory after processing the dummy input. This exposed the checker parameters and comparison target:

multiplier = 3394841907
shift      = 4
rotation   = 4
step       = 15
offset     = 11
target     = 042862c3031a121e7ce51a22126437c3f8

The original module itself remained unchanged. The instrumented files are available as instrumented.wasm (/C:/Users/aayus/Downloads/patina-solve/instrumented.wasm) and instrumented.wat (/C:/Users/aayus/Downloads/patina-solve/instrumented.wat).

## 5. Reverse the final byte-chaining stage

The checker’s last stage combines every byte with the preceding transformed byte, a four-bit rotation, and a per-position mask.

Because each output depends on the previous internal byte, this stage was reversed from the end of the target toward the beginning:

for (let i = 16; i >= 0; i--) {
    let current = target[i] ^ mask[i];
    intermediate[i] = current ^ rol8(previous, rotation);
    previous = current;
}

This recovers the 17 intermediate bytes that existed before the final chaining operation.

## 6. Reverse the state and permutation stage

For each position, the checker XORs the intermediate byte with the low byte of a changing 32-bit state:

character = intermediate[i] XOR (state AND 0xff)

It then stores that character at a permuted body position:

body_index = (i × step + offset) mod 17

Using the recovered parameters:

body_index = (i × 15 + 11) mod 17

After recovering each character, the state is updated with the checker’s constant table:

state =
    constant[i]
    + multiplier × (character XOR rotate_left_32(state, shift))

All arithmetic is performed modulo 2³².

Reversing this stage produces:

rU57_n3v3r_5l33p5

Adding the required wrapper gives:

HKSTR{rU57_n3v3r_5l33p5}

The complete implementation is saved in solve.js (/C:/Users/aayus/Downloads/patina-solve/solve.js).

## 7. Verify against the original checker

The recovered flag was passed to the original, unmodified patina.wasm through a small WASI-compatible runner.

Result:

{
  "flag": "HKSTR{rU57_n3v3r_5l33p5}",
  "output": "accept\n",
  "exitCode": 0
}

The result is also saved in result.json (/C:/Users/aayus/Downloads/patina-solve/result.json).

## Final flag

HKSTR{rU57_n3v3r_5l33p5}