# Dead Drop Writeup

Solved by Aayush Upadhyay

## Flag

SPECTRONA{Melody_is_very_chocolaty}

## Challenge Overview

The challenge Dead Drop involves extracting hidden data from a PNG image file. The hidden data is stored in the least significant bit of each pixel RGB values. Following the extracted URL leads to a video with a decoy flag, but the real clue is a social media handle that leads to the actual flag.

## Solution Steps

### Step 1: Extract the Signal from the PNG

The supplied dead_drop.png looks like an ordinary image. The hidden data is in the least significant bit of each pixel red, green, and blue values, read in RGB order across the image. Packing those bits into bytes gives:

28:https://youtu.be/0H89x6K0H4k

The prefix 28: is the URL length prefix.

### Step 2: Follow the First Video

The link opens "MOTIVATION!!!!!!!". The description said to follow Shounak_tt on social media. It also contained hexadecimal bytes that decode to:

SPECTRONA{YOU_GOT_THE_FLAG!!}

This is a decoy flag. The real clue is the Shounak_tt handle in the description.

### Step 3: Find Shounak_tt on Instagram

Search Instagram for shounak_tt. The profile includes a link in bio leading to another YouTube video.

### Step 4: Extract the Real Flag

The second video description or comments contains the real flag:

SPECTRONA{Melody_is_very_chocolaty}

## Key Takeaway

Multi-stage OSINT challenges often include decoy flags to test whether solvers follow all clues completely. Always verify suspicious flags and continue investigating all leads provided in the challenge.
