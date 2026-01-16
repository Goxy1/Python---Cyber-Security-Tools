# ARP-Spoofing – Man-in-the-Middle

## 📌 Overview

This project demonstrates how **ARP Spoofing** can be used to perform a **Man-in-the-Middle (MITM)** attack within a local network.  
It is implemented in **Python** and follows a step-by-step educational approach, starting from ARP fundamentals to building a functional ARP spoofer.

🚨 **IMPORTANT:**  
This project is created **strictly for educational purposes only**.  
It is intended to help students, security enthusiasts, and penetration testers understand how ARP works and how such attacks can be detected and prevented.

**Do NOT use this code on networks or systems you do not own or have explicit permission to test.**

---

## 🔍 What is ARP Spoofing (Man-in-the-Middle Attack)?

**ARP Spoofing**, also known as **ARP Poisoning**, is a network attack technique where an attacker manipulates the **Address Resolution Protocol (ARP)** to intercept, modify, or block network traffic between two devices.

This attack is commonly used to perform a **Man-in-the-Middle (MITM)** attack inside a **local network (LAN)**.

---

## 🧠 How ARP Works (Quick Recap)

ARP is used to map an **IP address** to a **MAC address** inside a local network.

Example:
- A device wants to send data to `192.168.1.1`
- It asks: *"Who has this IP?"*
- The owner responds with its **MAC address**
- The sender stores this information in its **ARP table**

⚠️ **ARP has no authentication mechanism**, which makes it vulnerable to abuse.

---

## 💣 What is ARP Spoofing?

In an ARP Spoofing attack, the attacker sends **forged ARP replies** to:
- The **victim**
- The **network gateway (router)**

The attacker convinces both devices that:
- The attacker’s MAC address belongs to the other party

As a result:
- The victim sends traffic to the attacker
- The gateway sends traffic to the attacker
- The attacker positions themselves **between both devices**

This effectively creates a **Man-in-the-Middle** scenario.

---

## 🕵️ Man-in-the-Middle (MITM) Explained

A **Man-in-the-Middle attack** occurs when an attacker secretly intercepts communication between two parties who believe they are communicating directly with each other.

In an ARP Spoofing MITM attack, the attacker can:
- 👀 **Sniff sensitive data** (passwords, cookies, credentials)
- ✏️ **Modify traffic in transit**
- 🚫 **Block or redirect traffic**
- 🎭 Perform **session hijacking**
- 🔓 Downgrade encrypted connections (in some scenarios)

All of this happens **without the victim noticing**.

---

## 📍 Why ARP Spoofing Works

ARP Spoofing is possible because:
- ARP does **not verify** the sender of ARP replies
- Devices **blindly trust** received ARP responses
- ARP tables can be **overwritten at any time**

Attackers exploit this trust-based protocol design.

---

## 🛡️ Why This Matters (Defensive Perspective)

Understanding ARP Spoofing is important because it helps security teams:
- Detect suspicious ARP behavior
- Implement protections such as:
  - Static ARP entries
  - Dynamic ARP Inspection (DAI)
  - Network segmentation
  - Encryption (HTTPS, VPNs)

Learning how attacks work is essential for **building effective defenses**.

---

## 🛠️ Technologies Used

- Python 3
- Networking fundamentals (ARP, IP, MAC)
- Packet manipulation libraries (e.g. `scapy`)

---

## ⚠️ Legal & Ethical Disclaimer

This repository is provided **for educational purposes only**.

- ❌ Do NOT use this project for illegal activities
- ❌ Do NOT run this code on networks you do not own or have explicit permission to test
- ✅ Use only in lab environments, test networks, or CTF scenarios

The author takes **no responsibility** for any misuse or damage caused by this code.

---

## 🚀 Getting Started

Example:
- Install required dependencies
- Run the script in a controlled lab environment

---

## 🤝 Contribution

This project is intended as a learning resource.  
Feel free to fork it and improve the code or documentation.
