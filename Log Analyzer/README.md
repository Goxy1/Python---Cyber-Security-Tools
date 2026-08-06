#🛡️ Log Analyzer

A lightweight Python-based log analysis tool for detecting basic suspicious activity in SSH authentication logs and Apache/Nginx web logs.

The script parses log files and looks for suspicious patterns such as:
1. Brute-force attempts, multiple failed login attempts from the same IP address within a short period of time
2. Web scanning a large number of HTTP 404 responses from the same IP address
3. Unusually high traffic, a high number of requests coming from a single IP address

The project is created for learning, automation, and cybersecurity research purposes.

##⚠️ Disclaimer

This tool is created for educational and ethical purposes only.
Do NOT use it on systems, servers, logs, or infrastructure that you do not own or do not have explicit permission to analyze.

By using this project, you agree that:
- You will only use it on authorized systems
- You are responsible for your own actions
- The author is not responsible for misuse, damage, data loss, or other consequences
- The author is not responsible for false positives or false negatives produced by the tool
- Unauthorized access, monitoring, or testing may be illegal and punishable by law

Use this software at your own risk.

##🔍 Features

This tool can detect:
- Detection	Description
- SSH Brute Force	Detects multiple failed SSH login attempts from the same IP
- Web Scanning	Detects a high number of HTTP 404 responses from the same IP
- High Traffic	Detects a high number of requests from a single IP
- Demo Logs	Generates sample SSH and web logs for testing

##⚙️ Requirements

Make sure you have:
- Python 3.8+
- No external Python packages are required

The project uses only Python standard libraries.

##🚀 Usage

SSH / Authentication Log

Analyze an existing SSH authentication log:
- python log_analyzer.py --file /path/to/auth.log --type auth

Example:
- python log_analyzer.py --file /var/log/auth.log --type auth

Apache / Nginx Web Log

Analyze an existing web access log:
- python log_analyzer.py --file /path/to/access.log --type web

Example:
- python log_analyzer.py --file /var/log/nginx/access.log --type web

##🧪 Demo Mode

The script can generate sample logs automatically for testing.

SSH Demo
- python log_analyzer.py --demo auth

This creates:
- demo_auth.log and automatically analyzes it for possible brute-force activity

Web Demo
python log_analyzer.py --demo web

This creates:
- demo_web.log and automatically analyzes it for suspicious web scanning activity

##🎯 Detection Thresholds

Default detection settings:
- BRUTE_FORCE_THRESHOLD = 5
- BRUTE_FORCE_WINDOW_MIN = 5
- SCAN_404_THRESHOLD = 10
- HIGH_TRAFFIC_THRESHOLD = 100

Brute Force
An alert is generated when at least:
- 5 failed login attempts
Occur from the same IP within:
- 5 minutes
- Web Scanning

An alert is generated when the same IP generates at least:
- 10 HTTP 404 responses
- High Traffic

An alert is generated when a single IP generates at least:
- 100 requests

Thresholds can be changed directly inside the Python script.

##📊 Example Output

[i] Loaded 20 lines from 'demo_web.log' (type: web)

[i] Parsed 20 web requests

============================================================
ANALYSIS RESULTS
============================================================
[POSSIBLE SCANNING] IP 198.51.100.23: 15 HTTP 404 responses (possible directory/path scanning activity)
============================================================

Example brute-force detection:

============================================================
ANALYSIS RESULTS
============================================================
[BRUTE FORCE] IP 203.0.113.55: 6 failed login attempts between ...
============================================================

##📁 Project Structure
Log-Analyzer/
│
├── log_analyzer.py
├── README.md
├── demo_auth.log
└── demo_web.log

The demo log files are automatically generated when demo mode is used.

##🎯 Purpose

This project is intended for:
- Cybersecurity learning
- Python scripting practice
- Log analysis
- SIEM fundamentals
- Security monitoring
- Detection engineering basics
- Incident detection experiments
- Blue Team practice

It is ideal for students, beginners, and anyone interested in learning how basic security detections work.

##🔐 Legal Notice

By using this repository, you acknowledge that:
- You will only analyze systems and logs you own or are authorized to access
- You are fully responsible for how you use the software
- The author is not responsible for misuse
- The author is not responsible for any damage or consequences caused by using or modifying the software
- This project is provided "as is", without any warranty
- Unauthorized security testing or monitoring may violate applicable laws

Use responsibly and only in authorized environments.