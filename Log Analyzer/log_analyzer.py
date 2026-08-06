#!/usr/bin/env python3

import argparse
import re
import random
from collections import defaultdict
from datetime import datetime, timedelta

# ---------------------------------------------------------------------------
# Detection threshold settings
# ---------------------------------------------------------------------------
BRUTE_FORCE_THRESHOLD = 5        # Number of failed login attempts
BRUTE_FORCE_WINDOW_MIN = 5       # Time window in minutes
SCAN_404_THRESHOLD = 10          # Number of 404 responses from the same IP considered suspicious scanning
HIGH_TRAFFIC_THRESHOLD = 100     # Total number of requests from a single IP in the log file

SSH_FAIL_REGEX = re.compile(
    r"(?P<month>\w{3})\s+(?P<day>\d+)\s+(?P<time>\d{2}:\d{2}:\d{2}).*"
    r"Failed password for (invalid user )?(?P<user>\S+) from (?P<ip>[\d.]+)"
)

APACHE_LOG_REGEX = re.compile(
    r'(?P<ip>[\d.]+) - - \[(?P<time>[^\]]+)\] "(?P<method>\S+) (?P<path>\S+) \S+" '
    r'(?P<status>\d{3}) (?P<size>\S+)'
)


def parse_auth_log(lines):
    """Parses SSH/auth logs and returns a list of failed login attempts: (ip, user, timestamp)."""
    events = []
    current_year = datetime.now().year
    for line in lines:
        match = SSH_FAIL_REGEX.search(line)
        if match:
            ts_str = f"{current_year} {match.group('month')} {match.group('day')} {match.group('time')}"
            try:
                ts = datetime.strptime(ts_str, "%Y %b %d %H:%M:%S")
            except ValueError:
                continue
            events.append((match.group("ip"), match.group("user"), ts))
    return events


def parse_web_log(lines):
    """Parses Apache/Nginx access logs and returns a list of (ip, status, path) entries."""
    events = []
    for line in lines:
        match = APACHE_LOG_REGEX.search(line)
        if match:
            events.append((match.group("ip"), int(match.group("status")), match.group("path")))
    return events


def detect_brute_force(events):
    """Groups failed login attempts by IP and looks for X attempts within a Y-minute window."""
    per_ip = defaultdict(list)
    for ip, user, ts in events:
        per_ip[ip].append((user, ts))

    alerts = []
    for ip, attempts in per_ip.items():
        attempts.sort(key=lambda a: a[1])
        for i in range(len(attempts)):
            window_start = attempts[i][1]
            window_end = window_start + timedelta(minutes=BRUTE_FORCE_WINDOW_MIN)
            count_in_window = sum(1 for _, ts in attempts if window_start <= ts <= window_end)
            if count_in_window >= BRUTE_FORCE_THRESHOLD:
                users_tried = sorted(set(u for u, ts in attempts if window_start <= ts <= window_end))
                alerts.append(
                    f"[BRUTE-FORCE] IP {ip}: {count_in_window} failed attempts "
                    f"between {window_start} i {window_end} (users: {', '.join(users_tried)})"
                )
                break  # One alert per IP is enoguh
    return alerts


def detect_web_anomalies(events):
    """Detects possible web scanning and unusually high traffic from individual IP addresses."""
    per_ip_total = defaultdict(int)
    per_ip_404 = defaultdict(int)

    for ip, status, path in events:
        per_ip_total[ip] += 1
        if status == 404:
            per_ip_404[ip] += 1

    alerts = []
    for ip, count_404 in per_ip_404.items():
        if count_404 >= SCAN_404_THRESHOLD:
            alerts.append(f"[POSSIBLE SCANNING] IP {ip}: {count_404} 404 responses (possible directory/path scanning activity)")

    for ip, total in per_ip_total.items():
        if total >= HIGH_TRAFFIC_THRESHOLD:
            alerts.append(f"[HIGH TRAFFIC] IP {ip}: {total} total requests in the log")

    return alerts


def generate_demo_auth_log(path="demo_auth.log"):
    """Detects possible scanning activity and unusually high traffic from individual IP addresses."""
    now = datetime.now()
    lines = []
    attacker_ip = "203.0.113.55"
    for i in range(8):
        ts = now - timedelta(minutes=8 - i)
        lines.append(
            f"{ts.strftime('%b %d %H:%M:%S')} server sshd[1000]: "
            f"Failed password for invalid user admin{i} from {attacker_ip} port 4000{i} ssh2"
        )
    normal_ip = "192.168.1.20"
    ts = now - timedelta(minutes=30)
    lines.append(
        f"{ts.strftime('%b %d %H:%M:%S')} server sshd[1001]: "
        f"Failed password for user milos from {normal_ip} port 55000 ssh2"
    )
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    return path


def generate_demo_web_log(path="demo_web.log"):
    """Creates a sample web access log containing an IP scanning non-existent paths."""
    now = datetime.now()
    lines = []
    scanner_ip = "198.51.100.23"
    for i in range(15):
        ts = now - timedelta(seconds=i * 2)
        lines.append(
            f'{scanner_ip} - - [{ts.strftime("%d/%b/%Y:%H:%M:%S +0000")}] '
            f'"GET /admin/config{i}.php HTTP/1.1" 404 512'
        )
    normal_ip = "192.168.1.30"
    for i in range(5):
        ts = now - timedelta(seconds=i * 5)
        lines.append(
            f'{normal_ip} - - [{ts.strftime("%d/%b/%Y:%H:%M:%S +0000")}] '
            f'"GET /index.html HTTP/1.1" 200 2048'
        )
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")
    return path


def main():
    parser = argparse.ArgumentParser(description="Log Analyzer / SIEM-lite")
    parser.add_argument("--file", help="Path of the log file")
    parser.add_argument("--type", choices=["auth", "web"], help="Log type: auth (SSH) or web (Apache/Nginx)")
    parser.add_argument("--demo", choices=["auth", "web"], help="Generate and analyze demo log")
    args = parser.parse_args()

    if args.demo:
        if args.demo == "auth":
            path = generate_demo_auth_log()
            log_type = "auth"
        else:
            path = generate_demo_web_log()
            log_type = "web"
        print(f"[i] Demo log generated: {path}\n")
    elif args.file and args.type:
        path = args.file
        log_type = args.type
    else:
        parser.print_help()
        return

    with open(path, "r", errors="ignore") as f:
        lines = f.readlines()

    print(f"[i] Loaded {len(lines)} lines from '{path}' (type: {log_type})\n")

    if log_type == "auth":
        events = parse_auth_log(lines)
        print(f"[i] Found {len(events)} failed login attempts\n")
        alerts = detect_brute_force(events)
    else:
        events = parse_web_log(lines)
        print(f"[i] Parsed {len(events)} web requests\n")
        alerts = detect_web_anomalies(events)

    print("=" * 60)
    print("ANALYSIS RESULTS")
    print("=" * 60)
    if alerts:
        for a in alerts:
            print(a)
    else:
        print("No suspicious activity detected.")
    print("=" * 60)


if __name__ == "__main__":
    main()
