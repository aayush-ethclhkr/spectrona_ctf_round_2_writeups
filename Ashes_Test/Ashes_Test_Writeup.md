# Ashes Test Writeup

Solved by Aayush Upadhyay

## Flag

B77W

## Challenge Overview

Category: OSINT

Points: 309

Challenge: Travelling from Ashes to Ashes… find the ICAO TYPE CODE for the return flight.

Answer format: ICAO aircraft type code (without flag braces)

## Solution Steps

### Step 1: Finding the Travel Account

The phrase "Ashes to Ashes" pointed toward the 2019 cricket Ashes series and a related travel write-up. Searching for the travelogue led to David Boyd blog post:

Travel Log – Ashes to Ashes — David Boyd
https://jdoboyd.com/2019/08/11/ashes2019/

The post documents his journey from Australia via Hong Kong to London for the Lords Ashes Test, followed by the return trip.

### Step 2: Identifying the Return Aircraft

The key entry is dated Tuesday, 20 August 2019. After leaving London for Heathrow, the author identifies the aircraft on the London-to-Hong-Kong return leg as:

Airline: Cathay Pacific (CX)
Aircraft: Boeing 777-367ER
Registration: B-KQP
Route: London (Heathrow) to Hong Kong

This was the crucial distinction: the challenge asked for the type of the aircraft on the relevant return flight, not simply the aircraft type typically used on a route between the UK and Australia.

### Step 3: Converting the Registration to an ICAO Type Code

The registration B-KQP was looked up in aircraft-tracking databases. Both Flightradar24 and Plane Finder identify it as a Cathay Pacific Boeing 777-367(ER), with type code B77W.

Aircraft Details:

| Field | Value |
|-------|-------|
| Registration | B-KQP |
| Operator | Cathay Pacific |
| Aircraft variant | Boeing 777-367(ER) |
| ICAO aircraft type designator | B77W |

The full Boeing model designation and the four-character ICAO type designator are different fields. The question specifically requested the latter.

### Step 4: Eliminating Incorrect Candidates

An initial route-based guess, B789 (Boeing 787-9), was incorrect. The correction was to rely on the specific aircraft registration given in the travel log instead of inferring aircraft type from a plausible airline route.

## Final Answer

B77W

## Key Takeaway

For flight-related OSINT challenges, trace the source to a specific flight and aircraft registration, then verify the required field in an aircraft database. A route, airline, and approximate date may still allow multiple aircraft types. A registration makes the type-code lookup precise.

## References

1. David Boyd — Travel Log: Ashes to Ashes
   https://jdoboyd.com/2019/08/11/ashes2019/
   20 August 2019 return journey and registration B-KQP

2. Flightradar24 — Aircraft B-KQP
   https://www.flightradar24.com/data/aircraft/b-kqp/
   Boeing 777-367(ER), type code B77W

3. Plane Finder — Aircraft B-KQP
   https://planefinder.net/data/aircraft/B-KQP
   Corroborating type-code record
