# 🛡️ Incident Response Tool (Learning Project)

A small Python **incident response / evidence collection** tool that creates incident records, gathers basic system evidence (network + processes + logs), stores metadata in a **SQLite** database, and generates a simple **text report**.

> ⚠️ **Educational use only**  
> This project is intended for **learning and lab use** (e.g., practicing incident response workflows).  
> Run it only on systems you own or have explicit permission to investigate.

---

## ✨ Features

- ✅ Creates and tracks incidents in a SQLite database  
- ✅ Collects basic **system information** (hostname, OS, architecture, etc.)
- ✅ Collects evidence:
  - Network connections (`netstat`)
  - ARP table (`arp -a`)
  - Running processes (`tasklist /v` on Windows, `ps aux` on Linux/macOS)
  - System logs (Linux: attempts to read `/var/log/auth.log`, Windows: placeholder file)
- ✅ Calculates **SHA-256 hashes** for evidence files
- ✅ Generates a human-readable **incident report** (`.txt`)

---

## ⚙️ Requirements

- Python **3.8+** recommended
- Uses only **standard library** modules (no pip installs required)

### 🖥️ System Commands Used
The script relies on OS tools being available:

- `netstat`
- `arp`
- `tasklist` (Windows) / `ps` (Linux/macOS)

> On some Linux distributions, `netstat` may not be installed by default (it’s part of `net-tools`).

---

## 📦 Installation

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd <your-repo-folder>
   ```
   (Optional) Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
   Activate it:
   - Windows (PowerShell):
    ```bash
    .\.venv\Scripts\Activate.ps1
    ```
   - Linux/macOS:
   ```bash
   source .venv/bin/activate
   ```

---


## ▶️ Usage

Run the script from the project directory:

- Windows:
    ```bash  
        python incident_response_tool.py
    ```

- macOS/Linux:
```bash
    python3 incident_response_tool.py
```

When executed, the script will:
1. Create a new incident (example values in __main__)
2. Collect evidence and write files into the current directory
3. Save metadata into a SQLite DB (incident_response_db.db)
4. Generate an incident report file


---

## 📄 Output Files

After running, you should see:
- 🗄️ Database
    - incident_response_db.db

- 📂 Evidence files
    - evidence_netstat_<incidentId>_<timestamp>.txt
    - evidence_arp_<incidentId>_<timestamp>.txt
    - evidence_processes_<incidentId>_<timestamp>.txt
    - evidence_auth_logs_<incidentId>_<timestamp>.txt (Linux only, if accessible)
    - evidence_event_logs_<incidentId>_<timestamp>.txt (Windows placeholder)
- 📊 Report
    - incident_report_<incidentId>_<timestamp>.txt


---

## ⚠️ Notes & Limitations

- Linux auth logs: reading /var/log/auth.log may require elevated permissions:
```bash
    sudo python3 incident_response_tool.py
```
- Windows event logs: current implementation is a placeholder and does not actually export Event Viewer logs
- This tool is intentionally minimal and does not implement secure evidence handling practices (e.g., write-once storage, chain of custody forms)


---

## 🎓 Learning Goals

This repository is useful for practicing:
- basic incident response workflow
- evidence collection automation
- storing artifacts + metadata
- hashing for integrity checks
- generating simple reports


---

## 🚫 Legal & Ethical Disclaimer

❗ **IMPORTANT**

This project is provided **STRICTLY FOR EDUCATIONAL AND RESEARCH PURPOSES ONLY**.

- ❌ Do NOT use this code to spy on users
- ❌ Do NOT deploy it on systems you do not own
- ❌ Do NOT use it to collect credentials or sensitive data
- ❌ Do NOT violate privacy laws or regulations

Using this software for **illegal, unethical, or unauthorized activities is strictly prohibited** and may result in legal consequences.

The author assumes **NO responsibility** for any misuse of this code.


---

## 📜 License

This project is licensed for **educational use only**.  
If you plan to reuse or modify it, ensure compliance with local laws and ethical guidelines.

---

## 🤝 Final Note

If you're learning cybersecurity, malware analysis, or Python internals — use this project responsibly.