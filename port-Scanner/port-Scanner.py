import socket
import sys
from datetime import datetime

def scan_port(host, port, timeout=1):
    """Try to connect to a single port. Return True if open."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))  # 0 = success = open
        sock.close()
        return result == 0
    except socket.error:
        return False

def resolve_host(target):
    """Convert hostname to IP if needed."""
    try:
        return socket.gethostbyname(target)
    except socket.gaierror:
        print(f"[ERROR] Cannot resolve hostname: {target}")
        sys.exit(1)

def scan_range(host, start_port, end_port):
    """Scan a range of ports and print open ones."""
    ip = resolve_host(host)
    print(f"\n{'='*50}")
    print(f"Target   : {host} ({ip})")
    print(f"Ports    : {start_port} - {end_port}")
    print(f"Started  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}\n")

    open_ports = []

    for port in range(start_port, end_port + 1):
        if scan_port(ip, port):
            print(f"[OPEN]  Port {port}")
            open_ports.append(port)
        else:
            print(f"[----]  Port {port}", end='\r')  # overwrite line for closed ports

    print(f"\n\nScan complete. {len(open_ports)} open port(s) found.")
    return open_ports

# --- Entry point ---
if __name__ == "__main__":
    target = input("Enter target IP or hostname: ").strip()
    start = int(input("Start port (e.g. 1): ").strip())
    end = int(input("End port (e.g. 1024): ").strip())
    scan_range(target, start, end)
