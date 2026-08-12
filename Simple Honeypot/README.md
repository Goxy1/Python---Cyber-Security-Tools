# Simple Honeypot

## 📌 Overview

This project is a simple multi-service honeypot written in Python designed to demonstrate how decoy network services can be used to detect connection attempts, network scanning, and unauthorized access attempts.

The script simulates basic SSH, FTP, and Telnet services on non-privileged ports and logs information about incoming connections and submitted data.

The repository exists **strictly for educational, cybersecurity training, and defensive research purposes**.

⚠️ **This honeypot should only be used in controlled or isolated environments such as a local virtual machine, home lab, or authorized test network.**

---

## ⚙️ How It Works (High-Level)

The honeypot starts several fake TCP services:

* **SSH** — default port `2222`
* **FTP** — default port `2121`
* **Telnet** — default port `2323`

When a client connects, the honeypot:

* Accepts the incoming TCP connection
* Sends a basic service-specific banner or login prompt
* Records the source IP address and source port
* Records the connection timestamp
* Logs submitted commands or credential attempts
* Rejects authentication attempts
* Stores activity inside `honeypot.log`

No real user authentication is performed.

Each service runs in its own thread, while incoming connections are handled using additional threads so multiple clients can be processed simultaneously.

---

## 📁 File Description

* **simple_honeypot.py**

  * Main honeypot script responsible for:

    * Starting fake SSH, FTP, and Telnet listeners
    * Accepting incoming TCP connections
    * Simulating basic service banners and login prompts
    * Recording connection attempts
    * Logging received data
    * Handling multiple connections using Python threads

* **honeypot.log**

  * Automatically created log file containing recorded honeypot activity
  * May contain:

    * Timestamp
    * Simulated service name
    * Source IP address
    * Source port
    * Submitted commands or credential attempts

---

## 🚀 Usage

Run the honeypot using the default ports:

```bash
python simple_honeypot.py
```

Default configuration:

```text
SSH     -> 2222
FTP     -> 2121
TELNET  -> 2323
```

Custom ports can also be specified:

```bash
python simple_honeypot.py --ssh-port 2222 --ftp-port 2121 --telnet-port 2323
```

To stop the honeypot:

```text
Ctrl+C
```

---

## 📝 Logging

Detected activity is written to:

```text
honeypot.log
```

Example log entries may look similar to:

```text
[2026-08-12 14:30:12] [SSH] Konekcija sa 192.168.1.50:52144 | Primljeni podaci: SSH-2.0-ExampleClient
[2026-08-12 14:31:05] [FTP] Konekcija sa 192.168.1.60:49321 | Primljeni podaci: USER admin
[2026-08-12 14:31:08] [FTP] Konekcija sa 192.168.1.60:49321 | Primljeni podaci: PASS example
```

The same events are also printed to the terminal while the honeypot is running.

⚠️ **Logs may contain submitted usernames, passwords, or other sensitive data. Store and handle them responsibly.**

---

## 🔌 Simulated Services

### SSH

The SSH honeypot sends a fake SSH banner:

```text
SSH-2.0-OpenSSH_8.9
```

It then records the first data received from the connecting client.

This is not a real SSH server and does not perform SSH encryption or authentication.

---

### FTP

The FTP honeypot simulates a minimal FTP server and reacts to commands such as:

```text
USER
PASS
```

Username and password attempts are logged before the service returns a failed authentication response.

No real FTP session is created.

---

### Telnet

The Telnet honeypot displays a basic login prompt:

```text
Ubuntu 22.04 LTS
login:
```

It records the supplied username and password before returning:

```text
Login incorrect
```

No actual system login occurs.

---

## 🚫 Legal & Ethical Disclaimer

❗ **IMPORTANT**

This project is provided **ONLY FOR EDUCATIONAL, LAB, AND AUTHORIZED SECURITY RESEARCH PURPOSES**.

* ❌ Do NOT deploy it on networks you do not own or have permission to test
* ❌ Do NOT use it to collect credentials from unsuspecting users
* ❌ Do NOT use collected information for unauthorized access
* ❌ Do NOT use the project for malicious surveillance or credential harvesting
* ❌ Do NOT expose it to the public internet without understanding the security and legal implications
* ❌ Do NOT treat captured credentials as permission to access another system

Use the honeypot only in environments where you have explicit authorization.

Depending on your jurisdiction, collecting network traffic, credentials, or identifying information may be subject to privacy, cybersecurity, or data protection laws.

The author takes **NO responsibility** for misuse of this software.

---

## 🧪 Suggested Lab Setup

A simple test environment can consist of two virtual machines:

```text
┌─────────────────────┐
│   Testing Machine   │
│                     │
│  SSH / FTP / Telnet │
│       Client        │
└──────────┬──────────┘
           │
           │ Isolated Lab Network
           │
┌──────────▼──────────┐
│  Honeypot Machine   │
│                     │
│  SSH    : 2222      │
│  FTP    : 2121      │
│  Telnet : 2323      │
│                     │
│  honeypot.log       │
└─────────────────────┘
```

This allows learners to observe how connection attempts appear in honeypot logs without exposing the system to an uncontrolled network.

---

## 📋 Requirements

The project uses only Python standard library modules:

```python
argparse
socket
threading
datetime
```

No additional third-party Python packages are required.

Recommended:

```text
Python 3.x
```

---

## 📜 License

This project is intended for **educational and defensive security use only**.

Ensure compliance with all applicable laws, organizational policies, and ethical guidelines before deploying or modifying it.