# 🔐 Password Policy Checker (Python)

## 📌 Overview

**Password Policy Checker** is an educational Python tool designed to evaluate password strength, enforce common security policies, estimate brute-force cracking time, and generate secure passwords and passphrases.

This project is intended for **cybersecurity education**, **defensive security awareness**, and **secure coding practice**.

---

## ✅ Features

- Password length validation  
- Uppercase character detection  
- Lowercase character detection  
- Numeric character validation  
- Special character validation  
- Detection of common passwords  
- Detection of sequential patterns (e.g. `abc`, `123`)  
- Detection of excessive repeated characters  
- Password scoring system (0–100)  
- Strength classification (Very Weak → Very Strong)  
- Password entropy calculation  
- Estimated brute-force cracking time  
- **Have I Been Pwned** password breach check (k-anonymity)  
- Secure password generation  
- Secure passphrase generation  
- Batch password checking from file  

---

## 🧩 How It Works

1. User selects an option from the interactive CLI menu  
2. The password is evaluated against defined security rules  
3. A score and strength level are calculated  
4. Password entropy and estimated crack time are computed  
5. Optional breach database check is performed  
6. Results and security recommendations are displayed  


---

## ▶️ Usage

Run the script:

python3 password_checker.py

Available options:
1. Check password strength
2. Generate a secure password
3. Generate a secure passphrase
4. Batch check passwords from a file
5. Exit


---

## ⚠️ Security & Privacy Notice

- Do NOT test real passwords used for personal or production systems
- Avoid using this tool with sensitive credentials
- Breach checks use a public API and should be treated accordingly


---

## 🚫 Legal & Ethical Disclaimer

IMPORTANT

-This project is provided STRICTLY FOR EDUCATIONAL AND DEFENSIVE PURPOSES ONLY.
- Do NOT use this tool without authorization
- Do NOT collect or store other people’s passwords
- Do NOT use this project for illegal or unethical activities
- The author assumes NO responsibility for misuse of this code.


---

## 📜 License

This project is intended for educational and research purposes only.
Ensure compliance with all applicable laws and ethical standards.

---

🤝 Final Note

Strong password policies significantly reduce security risks.
Learn responsibly. Use ethically.