#!/usr/bin/env python3

import argparse
import socket
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

DEFAULT_DIR_WORDLIST = [
    "admin", "login", "backup", "config", "config.php", "test", ".env",
    "uploads", "images", "api", "dashboard", "old", ".git", "robots.txt",
    "server-status", "phpinfo.php", "wp-admin", "database", "db.sql",
]

DEFAULT_SUB_WORDLIST = [
    "www", "mail", "ftp", "dev", "test", "staging", "api", "admin",
    "portal", "vpn", "webmail", "blog", "shop", "m", "cdn",
]

MAX_WORKERS = 20
REQUEST_TIMEOUT = 5


def load_wordlist(path, default):
    if not path:
        return default
    with open(path, "r") as f:
        return [line.strip() for line in f if line.strip()]


def check_path(base_url, word, timeout=REQUEST_TIMEOUT):
    url = f"{base_url.rstrip('/')}/{word.lstrip('/')}"
    try:
        resp = requests.get(url, timeout=timeout, allow_redirects=False, verify=False)
        if resp.status_code != 404:
            return (url, resp.status_code)
    except requests.RequestException:
        pass
    return None


def check_subdomain(domain, word):
    sub = f"{word}.{domain}"
    try:
        ip = socket.gethostbyname(sub)
        return (sub, ip)
    except socket.gaierror:
        return None


def run_dir_scan(base_url, wordlist):
    print(f"[i] Scanning paths: {base_url}")
    print(f"[i] Number of words in list: {len(wordlist)}\n")
    found = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(check_path, base_url, w): w for w in wordlist}
        for future in as_completed(futures):
            result = future.result()
            if result:
                url, status = result
                print(f"[+] {status} -> {url}")
                found.append(result)

    return found


def run_subdomain_scan(domain, wordlist):
    print(f"[i] Searching subdomains for: {domain}")
    print(f"[i] Number of words in list: {len(wordlist)}\n")
    found = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(check_subdomain, domain, w): w for w in wordlist}
        for future in as_completed(futures):
            result = future.result()
            if result:
                sub, ip = result
                print(f"[+] {sub} -> {ip}")
                found.append(result)

    return found


def main():
    parser = argparse.ArgumentParser(description="Directory / Subdomain Brute-forcer")
    subparsers = parser.add_subparsers(dest="mode", required=True)

    p_dir = subparsers.add_parser("dir", help="Brute-force path on website")
    p_dir.add_argument("--url", required=True, help="Simple URL, for example: http://localhost:5000")
    p_dir.add_argument("--wordlist", help="Path to file with list of paths")

    p_sub = subparsers.add_parser("subdomain", help="Brute-force subdomains with DNS")
    p_sub.add_argument("--domain", required=True, help="Simple domain, for example: example.com")
    p_sub.add_argument("--wordlist", help="Path to the file with lists of prefixes")

    args = parser.parse_args()

    if args.mode == "dir":
        wordlist = load_wordlist(args.wordlist, DEFAULT_DIR_WORDLIST)
        found = run_dir_scan(args.url, wordlist)
    else:
        wordlist = load_wordlist(args.wordlist, DEFAULT_SUB_WORDLIST)
        found = run_subdomain_scan(args.domain, wordlist)

    print(f"\n[i] Finished. Found {len(found)} results.")


if __name__ == "__main__":
    main()