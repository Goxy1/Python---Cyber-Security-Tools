#!/usr/bin/env python3

import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime

BASELINE_FILE = "baseline.json"
LOG_FILE = "fim_alerts.log"


def hash_file(filepath, block_size=65536):
    """Calculates the SHA-256 hash of the file."""
    sha256 = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for block in iter(lambda: f.read(block_size), b""):
                sha256.update(block)
        return sha256.hexdigest()
    except (PermissionError, FileNotFoundError):
        return None


def scan_directory(path):
    """Returns a dict {relative_path: hash} for all files in a folder (recursively)."""
    result = {}
    for root, _dirs, files in os.walk(path):
        for name in files:
            full_path = os.path.join(root, name)
            rel_path = os.path.relpath(full_path, path)
            file_hash = hash_file(full_path)
            if file_hash:
                result[rel_path] = file_hash
    return result


def save_baseline(state, baseline_path):
    with open(baseline_path, "w") as f:
        json.dump(state, f, indent=2)


def load_baseline(baseline_path):
    if not os.path.exists(baseline_path):
        print(f"[!] Baseline file '{baseline_path}' doesn't exists. First we run 'baseline' command.")
        sys.exit(1)
    with open(baseline_path, "r") as f:
        return json.load(f)


def log_alert(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {message}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def compare_states(old_state, new_state):
    """Returns (new_files, changed_files, deleted_files)."""
    old_files = set(old_state.keys())
    new_files = set(new_state.keys())

    added = new_files - old_files
    removed = old_files - new_files
    common = old_files & new_files
    modified = {f for f in common if old_state[f] != new_state[f]}

    return added, modified, removed


def cmd_baseline(args):
    print(f"[i] Creating baseline for a folder: {args.path}")
    state = scan_directory(args.path)
    save_baseline(state, args.baseline_file)
    print(f"[i] Baseline sacuvan u '{args.baseline_file}' ({len(state)} fajlova)")


def cmd_check(args):
    old_state = load_baseline(args.baseline_file)
    new_state = scan_directory(args.path)
    added, modified, removed = compare_states(old_state, new_state)

    if not (added or modified or removed):
        print("[OK] No changes. File integrity is preserved.")
        return

    for f in sorted(added):
        log_alert(f"NEW FILE: {f}")
    for f in sorted(modified):
        log_alert(f"CHANGED FAJL: {f}")
    for f in sorted(removed):
        log_alert(f"DELETED FAJL: {f}")


def cmd_watch(args):
    print(f"[i] Starting the continuous monitoring of the folder '{args.path}' on every {args.interval}s")
    print("[i] Ctrl+C for interruption \n")
    try:
        while True:
            cmd_check(args)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\n[i] Monitoring stopped.")


def main():
    parser = argparse.ArgumentParser(description="File Integrity Monitor")
    subparsers = parser.add_subparsers(dest="command", required=True)

    common_args = argparse.ArgumentParser(add_help=False)
    common_args.add_argument("--path", required=True, help="Path to folder that is being monitored")
    common_args.add_argument("--baseline-file", dest="baseline_file", default=BASELINE_FILE,
                              help="Path to baseline JSON file")

    p_baseline = subparsers.add_parser("baseline", parents=[common_args], help="Save the current state of folder")
    p_baseline.set_defaults(func=cmd_baseline)

    p_check = subparsers.add_parser("check", parents=[common_args], help="Compare the current state with the baseline")
    p_check.set_defaults(func=cmd_check)

    p_watch = subparsers.add_parser("watch", parents=[common_args], help="Continuously monitors the folder")
    p_watch.add_argument("--interval", type=int, default=10, help="Check interval in seconds")
    p_watch.set_defaults(func=cmd_watch)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()