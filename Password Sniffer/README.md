# Password Sniffer

## 📌 Overview

This project demonstrates how plaintext credentials can be intercepted from network traffic using a Password Sniffer.
It is implemented in Python and leverages packet sniffing techniques to extract usernames and passwords transmitted over unencrypted connections.

🚨 IMPORTANT:
This project is created strictly for educational purposes only.
It is intended to help students, cybersecurity learners, and security professionals understand how insecure network communications can expose sensitive data.

Do NOT use this code on networks or systems you do not own or have explicit permission to test.

---

## 🔍 What is a Password Sniffer?

A Password Sniffer is a tool that captures network traffic and analyzes packet contents to extract authentication data such as:
- Usernames
- Passwords
- Session credentials

This is possible when applications transmit data over unencrypted protocols such as HTTP, FTP, or Telnet.

---

## 🧠 How It Works (High-Level)

This script:
1. Listens to network traffic on a specified network interface
2. Inspects TCP packets containing raw payload data
3. Searches for common username and password field names
4. Extracts and decodes credentials found in HTTP requests
5. Prints captured credentials to the console

---

## 🧪 Credential Detection Logic

The sniffer searches packet payloads for commonly used form fields.

Username fields may include:
- username, user, login, email, userid, login_email, etc.

Password fields may include:
- password, pass, passwd, pwd, login_password, etc.

Regular expressions are used to identify these fields inside captured packets.

---

## 🔓 Why Password Sniffing is Possible

Password sniffing works because:
- Data is transmitted in plaintext
- No encryption (HTTPS/TLS) is used
- Traffic can be intercepted by anyone on the same network

Once HTTPS is used, this technique no longer works in the same way.

---

## 🛡️ Defensive Perspective

Understanding password sniffing helps defenders:
- Enforce HTTPS everywhere
- Use encrypted protocols
- Detect suspicious sniffing behavior
- Educate users about insecure networks

---

## 🛠️ Technologies Used

- Python 3
- Scapy
- Regular expressions
- urllib.parse

---

## ⚠️ Legal & Ethical Disclaimer

This repository is provided for educational purposes only.

- Do NOT use this project for illegal activities
- Do NOT sniff traffic on networks you do not own or have permission to test
- Use only in lab environments, test networks, or CTF scenarios

The author takes no responsibility for any misuse of this code.

---

## 🤝 Contribution

This project is intended as a learning resource.
Feel free to fork and improve the code or documentation.
