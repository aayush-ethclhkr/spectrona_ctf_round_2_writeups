# SPECTRONA — The Final Move

**Category:** Miscellaneous / Steganography  
**Difficulty:** Medium  
**Input:** `final_move.pgn` inside `SPECTRONA_FINAL_MOVE_PLAYER.zip`  
**Flag format:** `spectrona{...}`

## Recovered flag

**`spectrona{the_final_move_wan_the_board}`**

## Summary

The PGN contains a real historical chess score with five extra annotations. The moves identify the 1999 Kasparov–Topalov game; the final words of the added annotations spell **D H O N I**. This points to MS Dhoni. The sporting-history clue narrows the intended video to Dhoni's match-winning six in the 2011 Cricket World Cup final.

The description of the intended video contains a Base64-encoded flag. Decoding it gives `spectrona{the_final_move_wan_the_board}`. The result is reproduced exactly as encoded, including the spelling `wan`.

## 1. Inspect the supplied archive

List the archive before extracting it:

```bash
unzip -l SPECTRONA_FINAL_MOVE_PLAYER.zip
```

It contains `FINAL_MOVE.md` and `final_move.pgn`. Extract the files and read the challenge instructions and PGN:

```bash
mkdir final-move
unzip SPECTRONA_FINAL_MOVE_PLAYER.zip -d final-move
cd final-move
cat FINAL_MOVE.md
cat final_move.pgn
```

The challenge says the move sequence is genuine but the record has an added layer. The PGN comments are therefore evidence to inspect separately from the chess score.

## 2. Separate the annotations from the chess moves

Show only the brace-delimited comments:

```bash
grep -o '{[^}]*}' final_move.pgn
```

There are five added comments:

```text
The exchange looks tactical, but the first impression hides a later defense.
A quiet move can restore a fragile harmony.
The sacrifice changes the calculation for the opponent.
Material can be counted; its record remains in the notation.
The queen takes the rook, but the king hunt continues toward its inspiration.
```

Take the first letter of each comment's final word:

```text
defense     D
harmony     H
opponent    O
notation    N
inspiration I
```

The added layer spells **DHONI**. This is the lead for the next stage, not the flag itself.

## 3. Identify the genuine chess game

Ignore the comments and compare the moves. The score is the famous Garry Kasparov–Veselin Topalov game from Wijk aan Zee, 1999. The sequence includes the celebrated exchange sacrifice and finishes with `44. Qa7 1-0`.

For example, compare the supplied moves with a recorded copy of the game:

- [Kasparov–Topalov 1999 PGN](https://github.com/kerry-huang-nyu/chessRobot/blob/main/kasparov_topalov_1999.pgn)

This confirms that the chess notation is the genuine historical layer. The comments form a separate clue layer.

## 4. Follow DHONI into sporting history

The name points to Indian cricketer MS Dhoni. In the 2011 Cricket World Cup final against Sri Lanka, Dhoni hit the winning six in the 49th over. The ICC's account describes the shot and quotes the commentary call, “Dhoni finishes off in style.”

- [ICC: Greatest Moments — Final](https://www.icc-cricket.com/tournaments/cricketworldcup/news/icc-mens-cricket-world-cup-greatest-moments-final)

That supports the connection from the annotation acrostic to the event. The intended next step is to find the specific YouTube video and read its description, as the challenge objective states.

## 5. Find the intended video

Search for the event clue and the title **“Dhoni finishes off in style! | THE FINAL MOVE”**. The intended upload is by **Lets Talk With Shounak**:

- [YouTube video: Dhoni finishes off in style! | THE FINAL MOVE](https://www.youtube.com/watch?v=lP2kkML7SEk)

The description repeats the clues and ends with a Base64 string:

```text
c3BlY3Ryb25he3RoZV9maW5hbF9tb3ZlX3dhbl90aGVfYm9hcmR9
```

## 6. Decode the flag

Decode the string from the video description with the standard Base64 utility:

```bash
printf '%s' 'c3BlY3Ryb25he3RoZV9maW5hbF9tb3ZlX3dhbl90aGVfYm9hcmR9' | base64 -d
```

Output:

```text
spectrona{the_final_move_wan_the_board}
```

## Conclusion

```text
PGN move score          -> Kasparov–Topalov, Wijk aan Zee 1999
Annotation final words  -> D H O N I
DHONI                   -> MS Dhoni
Sporting history        -> winning six, 2011 Cricket World Cup final
YouTube description     -> Base64-encoded flag
Decoded flag            -> spectrona{the_final_move_wan_the_board}
```

## Final flag

```text
spectrona{the_final_move_wan_the_board}
```
