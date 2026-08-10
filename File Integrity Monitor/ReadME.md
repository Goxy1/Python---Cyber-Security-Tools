# File Integrity Monitor – SHA-256 File Change Detection

## 📌 Overview

This project implements a **File Integrity Monitor (FIM)** that tracks files inside a specified directory using **SHA-256 hashes**.

It detects:

* ➕ **New files**
* ✏️ **Modified files**
* 🗑️ **Deleted files**

The tool is written in **Python** and follows a simple baseline-based monitoring approach commonly used in cybersecurity and system integrity monitoring.

🚨 **IMPORTANT:**
This project is created **strictly for educational, cybersecurity learning, and CV/portfolio purposes**.

It is intended to demonstrate how file integrity monitoring works and how unauthorized or unexpected file changes can be detected.

---

## 🧠 How File Integrity Monitoring Works

This project uses **SHA-256 cryptographic hashes** to identify file changes.

Every file has its contents processed through the SHA-256 hashing algorithm.

Example:

```text
file.txt
   ↓
SHA-256
   ↓
a591a6d40bf420404a011733cfb7b190...
```

If even a small part of the file changes, its SHA-256 hash will also change.

The program compares previously stored hashes with newly calculated hashes to determine whether a file has been modified.

---

## ⚙️ How the Project Works

The program supports three operating modes:

### 1️⃣ Baseline

The `baseline` command scans the target directory recursively and calculates the SHA-256 hash of every accessible file.

The results are stored in:

```text
baseline.json
```

This file represents the trusted state of the monitored directory.

Example:

```bash
python file_integrity_monitor.py baseline --path ./watched_folder
```

---

### 2️⃣ Check

The `check` command scans the directory again and compares the current state with the previously saved baseline.

It detects:

* ➕ Files that did not exist in the baseline
* ✏️ Files whose SHA-256 hash has changed
* 🗑️ Files that existed in the baseline but are now missing

Example:

```bash
python file_integrity_monitor.py check --path ./watched_folder
```

If no changes are detected:

```text
[OK] No changes. File integrity is preserved.
```

---

### 3️⃣ Watch

The `watch` command performs continuous monitoring.

It repeatedly checks the directory at a specified interval.

Example:

```bash
python file_integrity_monitor.py watch --path ./watched_folder --interval 10
```

This checks the monitored directory every **10 seconds**.

Press:

```text
Ctrl+C
```

to stop monitoring.

---

## 🔄 Detection Process

The monitoring process can be summarized as:

```text
Monitored Folder
      ↓
Calculate SHA-256 Hashes
      ↓
Compare With baseline.json
      ↓
 ┌─────────────┬───────────────┬──────────────┐
 │ New File    │ Modified File │ Deleted File │
 └─────────────┴───────────────┴──────────────┘
      ↓
Generate Alert
      ↓
fim_alerts.log
```

---

## 🚨 Alert Logging

When a change is detected, the program prints an alert to the terminal and writes it to:

```text
fim_alerts.log
```

Example alerts:

```text
[2026-08-10 15:30:22] NEW FILE: test.txt
[2026-08-10 15:31:04] CHANGED FILE: config.txt
[2026-08-10 15:32:17] DELETED FILE: notes.txt
```

This creates a basic audit trail of detected file changes.

---

## 📂 Example Project Structure

```text
file-integrity-monitor/
│
├── file_integrity_monitor.py
├── baseline.json
├── fim_alerts.log
├── README.md
│
└── watched_folder/
    ├── file1.txt
    ├── file2.txt
    └── documents/
        └── example.txt
```

---

## 🛠️ Technologies Used

* Python 3
* `hashlib`
* SHA-256 hashing
* `argparse`
* `json`
* `os`
* `datetime`
* File system monitoring concepts

No external Python libraries are required.

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd file-integrity-monitor
```

### 2. Create a folder to monitor

```bash
mkdir watched_folder
```

Add some test files inside the folder.

### 3. Create the initial baseline

```bash
python file_integrity_monitor.py baseline --path ./watched_folder
```

### 4. Make a change

Try one of the following:

* Create a new file
* Edit an existing file
* Delete a file

### 5. Check file integrity

```bash
python file_integrity_monitor.py check --path ./watched_folder
```

### 6. Start continuous monitoring

```bash
python file_integrity_monitor.py watch --path ./watched_folder --interval 10
```

---

## 📄 Custom Baseline File

By default, the program uses:

```text
baseline.json
```

A different baseline file can be specified with:

```bash
--baseline-file
```

Example:

```bash
python file_integrity_monitor.py baseline --path ./watched_folder --baseline-file custom_baseline.json
```

Then use the same baseline file when checking:

```bash
python file_integrity_monitor.py check --path ./watched_folder --baseline-file custom_baseline.json
```

---

## 🎯 Educational Purpose

This project demonstrates several important cybersecurity and Python concepts:

* File integrity monitoring
* Cryptographic hashing
* Baseline comparison
* Recursive directory scanning
* Change detection
* Security logging
* Command-line argument parsing
* Continuous monitoring

It can be used as a beginner-friendly **Blue Team / defensive security project** for learning and portfolio development.

---

## ⚠️ Legal & Ethical Disclaimer

This repository is provided **for educational and authorized security purposes only**.

* ✅ Use it on your own systems
* ✅ Use it in lab environments
* ✅ Use it for learning, testing, and defensive monitoring
* ❌ Do not use it to access or monitor systems without authorization

The author takes **no responsibility** for misuse of this project.