# Hash Password Cracker

## 📌 Overview

This project demonstrates how hashed passwords can be brute-forced using a wordlist.
It is implemented in Python and uses the built-in `hashlib` library to compare hashes generated from a wordlist against a target hash.

🚨 IMPORTANT:
This project is created strictly for educational purposes only.
It is intended to help students and cybersecurity learners understand how weak passwords and poor hashing practices can be exploited.

Do NOT use this code on systems or data you do not own or have explicit permission to test.

---

## 🔍 What Does This Script Do?

The script attempts to crack a hashed password by:
- Taking a hash value as input
- Generating hashes from a wordlist
- Comparing each generated hash with the target hash
- Revealing the original plaintext password if a match is found

---

## 🧠 How It Works

1. The user selects the hash type (e.g. `md5` or `sha1`)
2. The user provides a path to a wordlist file
3. The user provides the hash value to crack
4. Each word from the wordlist is hashed using the selected algorithm
5. The generated hash is compared to the target hash
6. If a match is found, the plaintext password is printed

If no match is found, the script informs the user.

---

## 🔐 Supported Hash Algorithms

- MD5
- SHA1

⚠️ These hashing algorithms are considered weak and should not be used for storing passwords in real-world applications.

---

## 🔓 Why Hash Cracking Is Possible

Hash cracking works when:
- Weak or unsalted hashing algorithms are used
- Passwords are predictable or short
- Attackers have access to the hash value
- Wordlists contain common passwords

---

## 🛡️ Defensive Perspective

Understanding hash cracking helps defenders:
- Use strong, modern hashing algorithms (bcrypt, scrypt, Argon2)
- Implement salting
- Enforce strong password policies
- Prevent offline password attacks

---

## 🛠️ Technologies Used

- Python 3
- hashlib
- Wordlist files

---

## ⚠️ Legal & Ethical Disclaimer

This repository is provided for educational purposes only.

- Do NOT use this project for illegal activities
- Do NOT attempt to crack passwords you do not own
- Use only in lab environments, test systems, or CTF scenarios

The author takes no responsibility for any misuse of this code.

---

## 🤝 Contribution

This project is intended as a learning resource.
Feel free to fork and improve the code or documentation.
