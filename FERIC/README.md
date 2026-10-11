Flag: HKSTR{rU57_C4N_83_F3r1C_45_W311}

Triage. feric.wasm is a small WASI module that exports _start and feric_frame_digest. feric_frame_digest is never called, so it’s a decoy.
Read _start. It takes a 32-byte token shaped like HKSTR{ + 25 chars + }. The inner chars come from A-Za-z0-9_, with _ fixed at inner positions 4, 8, 11, 17 and 20. The other 20 chars go into a keyed hash whose output is compared to a stored 192-bit target.
Dump the constants. The key schedule doesn’t depend on the input, so I ran the module once and read all its tables out of memory.
Port and verify. I rewrote the hash in Python and checked it against the real module’s final state.
Solve the first 7 chars. They feed a chain that must equal 64 bits of the target. A meet-in-the-middle search found exactly one answer: rU57_C4N.
Solve the other 13 chars. The remaining stages (the 262,144-round loop and the mixing block) are all invertible. I ran them backwards from the target to get the required bytes, then tried each of the 62 possible values per position to find the match.
Confirm. The real module prints “FERIC structural validation passed” for this token, and fails if the last character is changed.