# Directory / Subdomain Brute-forcer

## 📌 Overview

This project is a simple directory and subdomain brute-forcing tool written in Python designed to demonstrate basic web content discovery and DNS enumeration techniques used during authorized security testing.

The script can test common web directories and files against a target URL, or attempt to discover subdomains by resolving common prefixes through DNS.

The repository exists **strictly for educational, cybersecurity training, and defensive research purposes**.

⚠️ **This tool should only be used in controlled environments, home labs, CTF environments, or against systems and domains you own or have explicit permission to test.**

---

## ⚙️ How It Works (High-Level)

The tool provides two operating modes:

* **Directory Enumeration** — tests common paths such as `/admin`, `/backup`, `/config.php`, and `/api`
* **Subdomain Enumeration** — tests prefixes such as `mail`, `dev`, `test`, and `staging` against a target domain

When running in directory mode, the tool:

* Loads directory and file names from a wordlist
* Builds a URL for each entry
* Sends HTTP GET requests to the target
* Does not follow redirects
* Reports responses that do not return HTTP `404`
* Uses multiple threads to process requests concurrently

When running in subdomain mode, the tool:

* Loads subdomain prefixes from a wordlist
* Combines each prefix with the target domain
* Attempts to resolve each hostname through DNS
* Displays successfully resolved subdomains
* Displays the resolved IP address
* Uses multiple threads to perform DNS lookups concurrently

If no external wordlist is provided, the script uses a small built-in default wordlist.

---

## 📁 File Description

* **dir_subdomain_bruteforcer.py**

  * Main script responsible for:

    * Parsing command-line arguments
    * Loading custom or built-in wordlists
    * Performing directory enumeration
    * Sending HTTP GET requests
    * Checking HTTP response status codes
    * Performing subdomain enumeration
    * Resolving hostnames through DNS
    * Handling multiple requests using `ThreadPoolExecutor`

* **wordlist_dirs.txt** *(optional)*

  * Custom directory and file wordlist
  * Each entry should be placed on a separate line

* **wordlist_subs.txt** *(optional)*

  * Custom subdomain prefix wordlist
  * Each prefix should be placed on a separate line

---

## 🚀 Usage

Run directory enumeration using the built-in wordlist:

```bash
python dir_subdomain_bruteforcer.py dir --url http://localhost:5000
```

Use a custom directory wordlist:

```bash
python dir_subdomain_bruteforcer.py dir --url http://localhost:5000 --wordlist wordlist_dirs.txt
```

Run subdomain enumeration using the built-in wordlist:

```bash
python dir_subdomain_bruteforcer.py subdomain --domain example.com
```

Use a custom subdomain wordlist:

```bash
python dir_subdomain_bruteforcer.py subdomain --domain example.com --wordlist wordlist_subs.txt
```

---

## 🔎 Directory Enumeration

In directory mode, the script creates a URL for every entry in the supplied wordlist.

Example wordlist:

```text
admin
login
backup
config
config.php
.env
api
dashboard
robots.txt
```

The resulting requests may look like:

```text
http://localhost:5000/admin
http://localhost:5000/login
http://localhost:5000/backup
http://localhost:5000/config.php
```

Any response with a status code other than `404` is displayed as a potentially interesting result.

Example output:

```text
[i] Skeniram putanje na: http://localhost:5000
[i] Broj reci u listi: 19

[+] 200 -> http://localhost:5000/admin
[+] 403 -> http://localhost:5000/.git
[+] 301 -> http://localhost:5000/dashboard

[i] Zavrseno. Pronadjeno 3 rezultata.
```

A non-404 response does not automatically mean that a resource is sensitive or accessible.

For example:

```text
200 -> Resource returned successfully
301 -> Permanent redirect
302 -> Temporary redirect
401 -> Authentication required
403 -> Access forbidden
404 -> Resource not found
```

---

## 🌐 Subdomain Enumeration

In subdomain mode, the script creates candidate hostnames using the following format:

```text
<word>.<domain>
```

Example wordlist:

```text
www
mail
ftp
dev
test
staging
api
admin
portal
vpn
```

For the domain:

```text
example.com
```

The tool may test hostnames such as:

```text
www.example.com
mail.example.com
dev.example.com
test.example.com
api.example.com
```

If a hostname successfully resolves through DNS, the subdomain and IP address are displayed.

Example output:

```text
[i] Searching subdomains for: example.com
[i] Number of words in list: 15

[+] www.example.com -> 93.184.216.34
[+] mail.example.com -> 192.0.2.10
[+] dev.example.com -> 192.0.2.20

[i] Finished. Found 3 results.
```

---

## 🧵 Threading

The script uses Python's:

```python
ThreadPoolExecutor
```

to perform multiple requests or DNS lookups simultaneously.

The maximum number of concurrent workers is configured as:

```python
MAX_WORKERS = 20
```

The HTTP request timeout is configured as:

```python
REQUEST_TIMEOUT = 5
```

This improves performance while limiting the number of simultaneous operations.

⚠️ **Even with a worker limit, automated enumeration can generate noticeable traffic and may trigger IDS, IPS, WAF, SIEM, or other security monitoring systems.**

---

## 🚫 Legal & Ethical Disclaimer

❗ **IMPORTANT**

This project is provided **ONLY FOR EDUCATIONAL, LAB, AND AUTHORIZED SECURITY RESEARCH PURPOSES**.

* ❌ Do NOT scan websites, domains, networks, or systems without authorization
* ❌ Do NOT enumerate third-party infrastructure without explicit permission
* ❌ Do NOT use discovered directories, files, or subdomains to gain unauthorized access
* ❌ Do NOT use discovered information for exploitation, credential attacks, or data theft
* ❌ Do NOT intentionally generate disruptive traffic against production systems
* ❌ Do NOT treat a publicly accessible website or domain as permission to test it

Use this tool only against systems and domains that you own or have explicit authorization to test.

Unauthorized scanning may violate computer misuse, cybersecurity, privacy, or data protection laws depending on your jurisdiction.

The author takes **NO responsibility** for misuse of this software.

---

## 📋 Requirements

The project uses the following Python standard library modules:

```python
argparse
socket
concurrent.futures
```

The project also requires:

```python
requests
```

Install it using:

```bash
pip install requests
```

Recommended:

```text
Python 3.x
```

---

## 📜 License

This project is intended for **educational and defensive security use only**.

Ensure compliance with all applicable laws, organizational policies, rules of engagement, and ethical guidelines before using or modifying it.