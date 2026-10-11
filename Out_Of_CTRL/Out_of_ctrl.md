SPECTRONA CTF 2026 — Out Of CTRL
Category: OSINT
Author: cursorhigh
Points: 370
Status: Solved (answer confirmed by the player)
Answer format: Domain only
Challenge files: None identified
Challenge
The challenge included a clue resembling "right 9 ctrl" and asked for the domain associated with the cryptocurrency wallet brand targeted in a compromise.
The important task was to identify the actor, trace the incident to the wallet, and then find the specific domain expected by the challenge.
Investigation
1. Identifying the username
The words "right 9 ctrl" suggested the username right9ctrl. Searching that exact name led to reporting on the 2018 npm event-stream supply-chain attack.
Useful OSINT search terms:
right9ctrl event-stream
right9ctrl flatmap-stream
right9ctrl cryptocurrency wallet
2. Tracing the compromise
The event-stream package received a malicious dependency, flatmap-stream, after maintenance access changed. Technical reporting linked right9ctrl to the incident. The malicious code was designed to target a particular cryptocurrency wallet application, Copay, rather than all users of event-stream indiscriminately.
The relevant relationship was:
right9ctrl
   ↓
npm event-stream / malicious flatmap-stream dependency
   ↓
Copay cryptocurrency wallet
3. Finding the expected domain
After identifying Copay, I searched for the wallet by name and checked associated domain references. The domain expected by the challenge was:
copaywallet.io
Important distinction: Historical BitPay materials also refer to copay.io as a distribution site for Copay. That is why copay.io may appear in research results, but it was not the answer accepted for this CTF challenge. The challenge-specific answer was confirmed by the player as copaywallet.io.
The appearance of copaywallet.io on a contemporary website does not independently establish that it was the original official BitPay/Copay domain at the time of the 2018 attack. For solving the challenge, the relevant fact is the accepted domain string; avoid treating unrelated wallet-download sites as automatically trustworthy.
Final Answer
copaywallet.io
Result: Correct, as confirmed by the player.
Key Takeaway
The useful OSINT chain was distinctive username → documented supply-chain attack → targeted wallet brand → challenge-specific domain. Identifying a brand is not always enough: domain-answer challenges can distinguish between a company's corporate site, an older product site, and the exact website intended by the question.
References
1. npm — Details about the event-stream incident — incident background.
2. Snyk — A post-mortem of the malicious event-stream backdoor — technical background and Copay targeting.
3. BitPay — New Copay developments, version 1.6.1 — historical evidence that copay.io also existed in connection with the wallet; not proof of the CTF answer.
4. Copay Wallet domain — current website for the submitted domain; its relationship to the historical BitPay product has not been independently established.