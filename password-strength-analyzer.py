import customtkinter as ctk
from tkinter import messagebox
import re
import hashlib
import random
import string
import requests

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Password Strength Checker")
app.geometry("500x450")

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def check_hibp(password)
    sha1_hash = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = sha1_hash[:5], sha1_hash[5:]

    try:
        response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}", timeout=5)
        response.raise_for_status()
    except requests.RequestException:
        return None
    
    for line in resposnse.text.splitlines():
        hash_suffix, count = line.split(':')
        if hash_suffix == suffix:
            return int(count)
        return 0
        

def suggest_password(password):
    suggestions = []
    if not re.search(r"[A-Z]", password):
        suggestions.append(random.choice(string.ascii_uppercase))
    if not re.search(r"[a-z]", password):
        suggestions.append(random.choice(string.ascii_lowercase))
    if not re.search(r"[0-9]", password):
        suggestions.append(random.choice(string.digits))
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        suggestions.append(random.choice("!@#$%^&*()"))
    while len(password) + len(suggestions) < 8:
        suggestions.append(random.choice(string.ascii_letters + string.digits + "!@#$%^&*()"))
    
    candidate = password + ''.join(suggestions)

    max_attempts = 5
    for attempt in range(max_attempts):
        breach_count = check_hibp(candidate)
        if breach_coount == 0 or breach_count is None:
            return candidate
        candidae += random.choice(string.ascii_letters + string.digits + "!@#$%^&*()")

    return candidate

def check_password():
    password = password_entry.get()
    strength = 0

    if len(password) >= 12:
        strength += 2
    elif len(password) >= 8:
        strength += 1
    
    if re.search(r"[A-Z]", password):
        strength += 1
    if re.search(r"[a-z]", password):
        strength += 1
    if re.search(r"[0-9]", password):
        strength += 1
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        strength += 1

    progress_bar.set(strength / 6)
    
    if strength <= 2:
        result_label.configure(text="Weak Password", text_color="red")
        suggestion = suggest_password(password)
        suggestion_label.configure(text=f"Suggestion: {suggestion}")
    elif strength <= 4:
        result_label.configure(text="Moderate Password", text_color="orange")
        suggestion_label.configure(text="Try adding symbols or numbers to improve strength")
    elif strength <= 5:
        result_label.configure(text="Strong Password", text_color="green")
        suggestion_label.configure(text="")
    else:
        result_label.configure(text="Perfect Password", text_color="pink")
        suggestion_label.configure(text="")

    breach_count = check_hibp(password)
    if breach_count is None:
        breach_label.configure(text="Couldn't reach breach database (check connection)", text_color="gray")
    elif breach_count > 0:
        breach_label.configure(text=f"⚠ Found in {breach_count:,} known breaches!", text_color="red")
    else:
        breach_label.configure(text="✓ Not found in known breaches", text_color="green")

def toggle_password():
    if password_entry.cget('show') == "*":
        password_entry.configure(show="")
        toggle_button.configure(text="Hide")
    else:
        password_entry.configure(show="*")
        toggle_button.configure(text="Show")

# UI elements
password_entry = ctk.CTkEntry(app, placeholder_text="Enter Password", show="*")
password_entry.pack(pady=20, padx=20, fill="x")

toggle_button = ctk.CTkButton(app, text="Show", width=60, command=toggle_password)
toggle_button.pack(pady=5)

check_button = ctk.CTkButton(app, text="Check Strength", command=check_password)
check_button.pack(pady=10)

progress_bar = ctk.CTkProgressBar(app, width=350)
progress_bar.set(0)
progress_bar.pack(pady=10)

result_label = ctk.CTkLabel(app, text="")
result_label.pack(pady=5)

suggestion_label = ctk.CTkLabel(app, text="", text_color="lightblue")
suggestion_label.pack(pady=5)

breach_label = ctk.CTkLabel(app, text="")
breach_label.pack(pady=5)

app.mainloop()
