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

- Passwords are **never stored** by this tool. Earlier versions of this
  project wrote a SHA-256 hash of each checked password to a local file;
  this has been removed, since an unlabeled, unsalted, one-way hash with
  no retrieval mechanism provided no real value and represented an
  unnecessary risk.
- Breach checking uses HIBP's k-anonymity model: the password is hashed
  locally with SHA-1, and only the first 5 characters of that hash are
  sent to the API. The full password is never transmitted.

## Possible future improvements

- Move the breach check to a background thread so the UI doesn't
  momentarily freeze while waiting on the network
- Add entropy-based scoring rather than relying solely on character-class
  counts
- Add a local common-password blocklist as a fast, offline first check
  before calling the API

Owner: Travis Farmer | Computer Science Enthusiast @ Georgia State University
