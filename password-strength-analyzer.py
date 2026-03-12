import math
import re
from typing import Dict, List

COMMON_PASSWORDS = {
    "password",
    "123456",
    "123456789",
    "qwerty",
    "abc123",
    "letmein",
    "welcome",
    "admin",
    "iloveyou",
    "password1",
}

KEYBOARD_PATTERNS = [
    "qwerty",
    "asdfgh",
    "zxcvbn",
    "123456",
    "abcdef",
]


def calculate_charset_size(password: str) -> int:
    """Estimate the possible character pool used in the password."""
    charset = 0

    if re.search(r"[a-z]", password):
        charset += 26
    if re.search(r"[A-Z]", password):
        charset += 26
    if re.search(r"\d", password):
        charset += 10
    if re.search(r"[^A-Za-z0-9]", password):
        charset += 32

    return max(charset, 1)


def calculate_entropy(password: str) -> float:
    """Estimate password entropy in bits."""
    if not password:
        return 0.0

    charset_size = calculate_charset_size(password)
    return len(password) * math.log2(charset_size)


def has_repeated_pattern(password: str) -> bool:
    """Check for repeated chunks like abcabc or 1212."""
    lowered = password.lower()
    for size in range(1, len(lowered) // 2 + 1):
        if len(lowered) % size == 0:
            chunk = lowered[:size]
            if chunk * (len(lowered) // size) == lowered:
                return True
    return False


def analyze_password(password: str) -> Dict[str, object]:
    """Return a detailed password strength analysis."""
    feedback: List[str] = []
    score = 0
    lowered = password.lower()

    if not password:
        return {
            "score": 0,
            "strength": "Very Weak",
            "entropy_bits": 0.0,
            "estimated_crack_time": "Instant",
            "feedback": ["Enter a password to analyze."],
        }

    # Length scoring
    length = len(password)
    if length >= 16:
        score += 4
    elif length >= 12:
        score += 3
    elif length >= 8:
        score += 2
    else:
        feedback.append("Use at least 12 characters; 16+ is even better.")

    # Character variety
    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add lowercase letters.")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add uppercase letters.")

    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("Add numbers.")

    if re.search(r"[^A-Za-z0-9]", password):
        score += 2
    else:
        feedback.append("Add special characters like !, @, or #.")

    # Penalties for common weaknesses
    if lowered in COMMON_PASSWORDS:
        score -= 4
        feedback.append("This is a very common password and is unsafe.")

    if any(pattern in lowered for pattern in KEYBOARD_PATTERNS):
        score -= 2
        feedback.append("Avoid common keyboard patterns like qwerty or 123456.")

    if re.search(r"(.)\1\1", password):
        score -= 2
        feedback.append("Avoid repeating the same character multiple times.")

    if has_repeated_pattern(password):
        score -= 2
        feedback.append("Avoid repeated patterns like abcabc or 1212.")

    if password.isalpha() or password.isdigit():
        score -= 2
        feedback.append("Do not use only letters or only numbers.")

    entropy = calculate_entropy(password)

    if entropy >= 80 and score >= 8:
        strength = "Very Strong"
    elif entropy >= 60 and score >= 6:
        strength = "Strong"
    elif entropy >= 45 and score >= 4:
        strength = "Moderate"
    elif entropy >= 28 and score >= 2:
        strength = "Weak"
    else:
        strength = "Very Weak"

    # Very rough offline cracking estimate based on entropy
    if entropy < 28:
        crack_time = "Seconds to minutes"
    elif entropy < 36:
        crack_time = "Hours to days"
    elif entropy < 45:
        crack_time = "Weeks to months"
    elif entropy < 60:
        crack_time = "Months to years"
    elif entropy < 80:
        crack_time = "Many years"
    else:
        crack_time = "Extremely long time"

    return {
        "score": max(score, 0),
        "strength": strength,
        "entropy_bits": round(entropy, 2),
        "estimated_crack_time": crack_time,
        "feedback": feedback if feedback else ["Good job. This password looks strong."],
    }


def main() -> None:
    print("Password Strength Analyzer")
    print("Type 'quit' to exit.\n")

    while True:
        password = input("Enter a password to analyze right now or else young boy: ")
        if password.lower() == "quit":
            print("Goodbye.")
            break

        result = analyze_password(password)
        print("\n--- Analysis ---")
        print(f"Strength: {result['strength']}")
        print(f"Score: {result['score']}")
        print(f"Entropy: {result['entropy_bits']} bits")
        print(f"Estimated crack time: {result['estimated_crack_time']}")
        print("Feedback:")
        for item in result["feedback"]:
            print(f"- {item}")
        print()


if __name__ == "__main__":
    main()