# Password Strength Analyzer

A desktop GUI tool that scores password strength in real time and checks
whether a password has appeared in known data breaches — built with
Python, Tkinter (CustomTkinter), and the [Have I Been Pwned](https://haveibeenpwned.com/API/v3)
API.

## Features

- **Real-time strength scoring** — scores passwords out of 6 points based on:
  - Length (8+ characters, 12+ characters)
  - Uppercase letters
  - Lowercase letters
  - Numbers
  - Symbols
- **4-tier strength rating** — Weak, Moderate, Strong, or Perfect, shown with
  a color-coded label and a progress bar
- **Breach detection** — checks the password against the Have I Been Pwned
  database using k-anonymity (only a 5-character hash prefix is ever sent
  over the network — the full password and full hash never leave your
  machine)
- **Smart suggestions** — for weak passwords, generates a stronger candidate
  by filling in missing character types, then verifies the suggestion
  itself isn't already in a known breach before showing it to you
- **Show/Hide toggle** — reveal or mask the password field as you type

## How it works

1. Enter a password in the input field
2. (Optional) Click "Show"/"Hide" to toggle plaintext visibility
3. Click "Check Strength"
4. The app will:
   - Score the password and update the progress bar and strength label
   - If the password is weak, generate and display a stronger suggested
     alternative
   - If the password is strong but not perfect, tell you the single most
     impactful thing to add (e.g. a symbol, or more length)
   - Query the HIBP API and report whether the password has been seen in
     known data breaches, and how many times

## Installation

```bash
pip install customtkinter requests
```

## Usage

```bash
python password_check.py
```

## Requirements

- Python 3.8+
- `customtkinter`
- `requests`
- An internet connection (required for breach checking)

## Notes on security

- Passwords are **never stored** by this tool.
- Breach checking uses HIBP's k-anonymity model: the password is hashed
  locally with SHA-1, and only the first 5 characters of that hash are
  sent to the API. The full password is never transmitted.

## Deep dive: how the k-anonymity breach check actually works

This is the core piece of the project worth being able to explain in detail.

The problem: you want to know if a password has appeared in a data breach,
but you don't want to send the plaintext password (or anything that
uniquely identifies it) to a third-party server. Have I Been Pwned solves
this with a technique borrowed from the k-anonymity model.

Step by step, here's what `check_hibp()` does:

1. **Hash locally.** The password is hashed with SHA-1:
   `hashlib.sha1(password.encode()).hexdigest().upper()`. This produces a
   40-character hex string. SHA-1 is used here specifically because it's
   the algorithm HIBP's API is built around — not because it's a good
   choice for storing passwords (it isn't; it's fast and crackable, which
   is exactly why it's fine for this one-way lookup use case, but wrong
   for actual credential storage).
2. **Split the hash.** The 40-character hash is split into the first 5
   characters (`prefix`) and the remaining 35 (`suffix`).
3. **Send only the prefix.** A GET request goes to
   `https://api.pwnedpasswords.com/range/{prefix}`. That's it — 5
   characters of a hash, nothing else. No password, no full hash, no
   username, no identifying metadata.
4. **The API returns a range, not an answer.** Because only 5 hex
   characters were sent, the API can't know which exact password you're
   checking — it responds with *every* breached hash in its database that
   starts with those same 5 characters, typically several hundred to a
   few thousand entries, each formatted as `SUFFIX:COUNT`.
5. **Compare locally.** The app loops through that returned list and
   checks whether your password's actual `suffix` appears anywhere in it.
   If it does, the breach count is returned. If not, the password (as far
   as HIBP's database knows) is clean.

The key privacy property: the server only ever learns "someone is curious
about hashes starting with `5BAA6`" — a set shared by many thousands of
different possible passwords — never which specific password you typed.
This is the same underlying idea as k-anonymity in data privacy more
broadly: you achieve anonymity by being indistinguishable from a group of
size k, rather than by encrypting or hiding the query itself.

This is also why `suggest_password()` calls `check_hibp()` on its own
generated candidates before showing them to the user: a "stronger"
password that satisfies the character-variety rules (uppercase, digit,
symbol, length) can still be a well-known breached password, like
`Password123!`. The suggestion loop mutates and re-checks up to 5 times
until it produces a candidate confirmed absent from the breach database
(or gives up and returns its best attempt if the API is unreachable).

## Decision log: removing the "Save Password Securely" feature

An earlier version of this tool included a checkbox that, when checked,
wrote a SHA-256 hash of the entered password to a local `passwords.txt`
file on every check.

This was removed, for a few concrete reasons:

- **No label.** The file stored a raw list of hashes with no associated
  username, site, or timestamp — there was no way to know which hash
  belonged to which account or password.
- **No retrieval path.** Hashing is one-way by design. Even with perfect
  labeling, there was no way to recover the original password from its
  hash — so this didn't function as a password manager or vault in any
  usable sense.
- **No salt.** The hash was computed with plain `hashlib.sha256()`, with
  no per-password salt — a meaningful gap if this were ever repurposed
  into something storing real credentials at rest.
- **Ran on every check, not once.** Since it was tied to the "Check
  Strength" button rather than a deliberate "save" action, the same
  password could be appended to the file repeatedly with no
  deduplication.

Rather than patch these issues into a feature with no clear purpose, the
feature was removed entirely and replaced with the HIBP breach check —
which uses the same underlying skill (hashing a password for a one-way
lookup) but in a way that provides genuine value to the user, with a
privacy model (k-anonymity) that's actually appropriate for the problem.


## Possible future improvements

- Move the breach check to a background thread so the UI doesn't
  momentarily freeze while waiting on the network
- Add entropy-based scoring rather than relying solely on character-class
  counts
- Add a local common-password blocklist as a fast, offline first check
  before calling the API

Owner: Travis Farmer | Computer Science Enthusiast @ Georgia State University
