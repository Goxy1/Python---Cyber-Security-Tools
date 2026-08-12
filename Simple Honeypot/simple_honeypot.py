#!/usr/bin/env python3

import argparse
import socket
import threading
from datetime import datetime

LOG_FILE = "honeypot.log"
log_lock = threading.Lock()


def log_event(service, ip, port, data=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    clean_data = data.replace("\n", " ").replace("\r", " ").strip()
    line = f"[{timestamp}] [{service}] Konekcija sa {ip}:{port}"
    if clean_data:
        line += f" | Loaded_data: {clean_data[:200]}"
    with log_lock:
        print(line)
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")


def handle_ssh_connection(conn, addr):
    """Simulates the SSH banner and records 'login' attempts (plaintext, because it is a fake service)."""
    ip, port = addr
    try:
        conn.sendall(b"SSH-2.0-OpenSSH_8.9\r\n")
        conn.settimeout(15)
        data = conn.recv(1024)
        log_event("SSH", ip, port, data.decode(errors="ignore"))
    except (socket.timeout, ConnectionResetError):
        log_event("SSH", ip, port, "(connection lost / no data)")
    finally:
        conn.close()


def handle_ftp_connection(conn, addr):
    """Simulates an FTP service and logs USER/PASS commands."""
    ip, port = addr
    try:
        conn.sendall(b"220 ProFTPD 1.3.5 Server ready.\r\n")
        conn.settimeout(20)
        buffer = ""
        while True:
            data = conn.recv(1024)
            if not data:
                break
            text = data.decode(errors="ignore")
            buffer += text
            log_event("FTP", ip, port, text)
            if text.upper().startswith("USER"):
                conn.sendall(b"331 Password required\r\n")
            elif text.upper().startswith("PASS"):
                conn.sendall(b"530 Login incorrect\r\n")
            else:
                conn.sendall(b"500 Unknown command\r\n")
    except (socket.timeout, ConnectionResetError):
        pass
    finally:
        conn.close()


def handle_telnet_connection(conn, addr):
    """Simulates a Telnet login prompt."""
    ip, port = addr
    try:
        conn.sendall(b"Ubuntu 22.04 LTS\r\nlogin: ")
        conn.settimeout(20)
        data = conn.recv(1024)
        log_event("TELNET", ip, port, f"login={data.decode(errors='ignore').strip()}")
        conn.sendall(b"Password: ")
        data = conn.recv(1024)
        log_event("TELNET", ip, port, f"password={data.decode(errors='ignore').strip()}")
        conn.sendall(b"\r\nLogin incorrect\r\n")
    except (socket.timeout, ConnectionResetError):
        pass
    finally:
        conn.close()


def start_listener(service_name, port, handler):
    """Starts a TCP listener on the given port in a separate thread for each connection."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("0.0.0.0", port))
    sock.listen(5)
    print(f"[i] {service_name} honeypot listens on port {port}")

    while True:
        try:
            conn, addr = sock.accept()
            t = threading.Thread(target=handler, args=(conn, addr), daemon=True)
            t.start()
        except OSError:
            break


def main():
    parser = argparse.ArgumentParser(description="Simple multi-service honeypot")
    parser.add_argument("--ssh-port", type=int, default=2222, help="Port for the fake SSH service")
    parser.add_argument("--ftp-port", type=int, default=2121, help="Port for the fake FTP service")
    parser.add_argument("--telnet-port", type=int, default=2323, help="Port for the fake Telnet service")
    args = parser.parse_args()

    services = [
        ("SSH", args.ssh_port, handle_ssh_connection),
        ("FTP", args.ftp_port, handle_ftp_connection),
        ("TELNET", args.telnet_port, handle_telnet_connection),
    ]

    threads = []
    for name, port, handler in services:
        t = threading.Thread(target=start_listener, args=(name, port, handler), daemon=True)
        t.start()
        threads.append(t)

    print(f"[i] Honeypot running. Logs are stored in '{LOG_FILE}'. Ctrl+C to exit.\n")
    try:
        while True:
            threading.Event().wait(1)
    except KeyboardInterrupt:
        print("\n[i] Honeypot stopeped.")


if __name__ == "__main__":
    main()