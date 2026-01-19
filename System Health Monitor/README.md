# System Health & Security Monitor (Python)

## 📌 Project Overview

This project is a **Python-based system monitoring and security awareness tool** designed to continuously observe system health metrics and detect potentially suspicious activity on a host machine.

It combines **resource monitoring** (CPU, memory, disk) with **basic security-oriented checks**, such as:
- Detection of suspicious open network ports
- Identification of potentially dangerous running processes
- Centralized logging of system state and alerts
- Optional email alerting (placeholder for integration)

The project is intended for **educational, defensive, and monitoring purposes**.

---

## 🛡️ Core Features

### System Health Monitoring
- CPU usage monitoring with configurable thresholds
- Memory usage monitoring
- Disk usage monitoring
- Periodic health checks at fixed intervals

### Security-Oriented Checks
- Detection of listening services on commonly targeted ports  
  *(e.g. SSH, RDP, SMB, NetBIOS)*
- Detection of suspicious process names  
  *(e.g. netcat, nmap, metasploit — configurable list)*
- Alert generation for abnormal or potentially risky behavior

### Alerting & Logging
- Structured alerts with:
  - Type
  - Timestamp
  - Threshold
  - Human-readable message
- JSON-based logging to a local log file
- Email alert framework (SMTP placeholder for future integration)

---

## 📁 Project Structure

- **system_monitor.py**
  - Main application file
  - Contains the `SystemMonitor` class and monitoring loop
- **system_monitor.log**
  - Automatically generated log file
  - Stores system snapshots and alerts in JSON format

---

## ⚙️ How It Works (High-Level)

1. The monitor runs in a continuous loop (default: every 30 seconds)
2. Each cycle performs:
   - CPU, memory, and disk usage checks
   - Network connection analysis
   - Process inspection
3. Any detected anomaly generates a structured alert
4. Alerts are:
   - Printed to the console
   - Logged to a file
   - Prepared for email notification
5. On shutdown, a summary report is displayed

---

## 🎯 Intended Use Cases

This project is suitable for:
- Cybersecurity learning and labs
- Blue team / defensive security practice
- System monitoring demonstrations
- SOC or IR training environments
- Python system programming education

It is **not a replacement for enterprise-grade monitoring solutions**, but a strong foundation for understanding how such tools work internally.

---

## 🚫 Legal & Ethical Disclaimer

❗ **IMPORTANT**

This project is provided **STRICTLY FOR EDUCATIONAL AND DEFENSIVE PURPOSES ONLY**.

- ❌ Do NOT use it to spy on users
- ❌ Do NOT deploy without authorization
- ❌ Do NOT rely on it as a production security solution
- ❌ Do NOT modify it for offensive or intrusive activities

All monitoring should be performed **only on systems you own or have explicit permission to monitor**.

The author assumes **NO responsibility** for misuse of this code.

---

## 🧠 Security Note

Understanding how systems behave under normal and abnormal conditions is essential for:
- Detecting intrusions
- Recognizing early signs of compromise
- Improving incident response readiness

**Good defense starts with visibility.**

---

## 🚀 Future Improvements (Ideas)

- Proper SMTP configuration for real email alerts
- Alert severity levels
- Export to SIEM / JSON endpoint
- OS-specific disk handling
- Rule-based or anomaly-based detection
- Dashboard or API interface

---

## 📜 License

This project is intended for **educational and research use only**.  
Ensure compliance with local laws, regulations, and ethical standards.

---

## 🤝 Final Note

If you're learning **cybersecurity, SOC operations, or system monitoring**, this project provides a solid and realistic starting point.

**Monitor responsibly. Defend ethically.**
