import socket
import argparse
import threading
from datetime import datetime
from queue import Queue

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 443: "HTTPS",
    445: "SMB", 3306: "MySQL", 3389: "RDP", 8080: "HTTP-Alt"
}

open_ports = []
queue = Queue()
lock = threading.Lock()
print_lock = threading.Lock()

def grab_banner(ip, port):
    try:
        s = socket.socket()
        s.settimeout(1)
        s.connect((ip, port))
        banner = s.recv(1024).decode().strip()
        s.close()
        return banner
    except:
        return None

def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((ip, port))
        sock.close()
        if result == 0:
            service = COMMON_PORTS.get(port, "Unknown")
            banner = grab_banner(ip, port)
            with lock:
                open_ports.append((port, service, banner))
            with print_lock:
                if banner:
                    print(f"  [OPEN] Port {port} ({service}) — {banner}")
                else:
                    print(f"  [OPEN] Port {port} ({service})")
    except:
        pass

def worker(ip):
    while not queue.empty():
        port = queue.get()
        scan_port(ip, port)
        queue.task_done()

def scan(ip, start_port, end_port, threads=100):
    print(f"\n{'='*50}")
    print(f"  Target   : {ip}")
    print(f"  Ports    : {start_port} - {end_port}")
    print(f"  Threads  : {threads}")
    print(f"  Started  : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}\n")

    for port in range(start_port, end_port + 1):
        queue.put(port)

    thread_list = []
    for _ in range(min(threads, end_port - start_port + 1)):
        t = threading.Thread(target=worker, args=(ip,))
        t.daemon = True
        thread_list.append(t)
        t.start()

    for t in thread_list:
        t.join()

    open_ports.sort(key=lambda x: x[0])

    print(f"\n{'='*50}")
    print(f"  Scan complete. {len(open_ports)} open ports found.")
    print(f"  Finished : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}\n")

def save_report(ip):
    filename = f"scan_{ip}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, "w") as f:
        f.write(f"Scan Report — {ip}\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        for port, service, banner in open_ports:
            if banner:
                f.write(f"[OPEN] Port {port} ({service}) — {banner}\n")
            else:
                f.write(f"[OPEN] Port {port} ({service})\n")
    print(f"  Report saved to {filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Network Scanner")
    parser.add_argument("ip", help="Target IP address")
    parser.add_argument("-s", "--start", type=int, default=1, help="Start port")
    parser.add_argument("-e", "--end", type=int, default=1024, help="End port")
    parser.add_argument("-t", "--threads", type=int, default=100, help="Threads")
    parser.add_argument("-r", "--report", action="store_true", help="Save report")
    args = parser.parse_args()

    scan(args.ip, args.start, args.end, args.threads)

    if args.report:
        save_report(args.ip)