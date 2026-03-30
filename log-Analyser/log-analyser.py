import re
import argparse
from collections import defaultdict
from datetime import datetime

# Thresholds
BRUTE_FORCE_THRESHOLD = 10   # failed attempts from same IP
SCAN_THRESHOLD = 20          # requests from same IP in short time
ERROR_THRESHOLD = 15         # 404s from same IP

def parse_log(filepath):
    entries = []
    # Apache/Nginx combined log format
    pattern = re.compile(
        r'(\d+\.\d+\.\d+\.\d+).*\[(.+?)\] "(\w+) (.+?) HTTP.*?" (\d+)'
    )
    try:
        with open(filepath, "r") as f:
            for line in f:
                match = pattern.search(line)
                if match:
                    entries.append({
                        "ip": match.group(1),
                        "time": match.group(2),
                        "method": match.group(3),
                        "path": match.group(4),
                        "status": int(match.group(5))
                    })
    except FileNotFoundError:
        print(f"[ERROR] File not found: {filepath}")
        exit(1)
    return entries

def analyse(entries):
    ip_requests = defaultdict(int)
    ip_404s = defaultdict(int)
    ip_401s = defaultdict(int)
    status_counts = defaultdict(int)
    path_hits = defaultdict(int)
    suspicious = []

    for entry in entries:
        ip = entry["ip"]
        status = entry["status"]
        path = entry["path"]

        ip_requests[ip] += 1
        status_counts[status] += 1
        path_hits[path] += 1

        if status == 404:
            ip_404s[ip] += 1
        if status == 401:
            ip_401s[ip] += 1

    # Detect brute force (too many 401s)
    for ip, count in ip_401s.items():
        if count >= BRUTE_FORCE_THRESHOLD:
            suspicious.append({
                "type": "Possible Brute Force",
                "ip": ip,
                "detail": f"{count} failed auth attempts (401s)"
            })

    # Detect scanning (too many 404s)
    for ip, count in ip_404s.items():
        if count >= ERROR_THRESHOLD:
            suspicious.append({
                "type": "Possible Directory Scan",
                "ip": ip,
                "detail": f"{count} not found errors (404s)"
            })

    # Detect high request volume
    for ip, count in ip_requests.items():
        if count >= SCAN_THRESHOLD:
            suspicious.append({
                "type": "High Request Volume",
                "ip": ip,
                "detail": f"{count} total requests"
            })

    return {
        "total_requests": len(entries),
        "ip_requests": ip_requests,
        "ip_404s": ip_404s,
        "ip_401s": ip_401s,
        "status_counts": status_counts,
        "top_paths": path_hits,
        "suspicious": suspicious
    }

def print_report(results, filepath):
    print(f"\n{'='*55}")
    print(f"  Log Analysis Report")
    print(f"  File     : {filepath}")
    print(f"  Time     : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*55}\n")

    print(f"  Total Requests : {results['total_requests']}")
    print(f"  Unique IPs     : {len(results['ip_requests'])}")

    print(f"\n  --- Status Code Breakdown ---")
    for status, count in sorted(results['status_counts'].items()):
        print(f"  {status} : {count} requests")

    print(f"\n  --- Top 5 Most Active IPs ---")
    sorted_ips = sorted(results['ip_requests'].items(),
                        key=lambda x: x[1], reverse=True)[:5]
    for ip, count in sorted_ips:
        print(f"  {ip} : {count} requests")

    print(f"\n  --- Top 5 Most Requested Paths ---")
    sorted_paths = sorted(results['top_paths'].items(),
                          key=lambda x: x[1], reverse=True)[:5]
    for path, count in sorted_paths:
        print(f"  {path} : {count} hits")

    if results['suspicious']:
        print(f"\n  --- Suspicious Activity Detected ---")
        for item in results['suspicious']:
            print(f"\n  [!] {item['type']}")
            print(f"      IP     : {item['ip']}")
            print(f"      Detail : {item['detail']}")
    else:
        print(f"\n  No suspicious activity detected.")

    print(f"\n{'='*55}\n")

def save_report(results, filepath):
    outfile = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(outfile, "w") as f:
        f.write(f"Log Analysis Report\n")
        f.write(f"File: {filepath}\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(f"Total Requests : {results['total_requests']}\n")
        f.write(f"Unique IPs     : {len(results['ip_requests'])}\n\n")
        if results['suspicious']:
            f.write("Suspicious Activity:\n")
            for item in results['suspicious']:
                f.write(f"\n[!] {item['type']}\n")
                f.write(f"    IP     : {item['ip']}\n")
                f.write(f"    Detail : {item['detail']}\n")
    print(f"  Report saved to {outfile}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Web Server Log Analyser")
    parser.add_argument("log", help="Path to log file")
    parser.add_argument("-r", "--report", action="store_true",
                        help="Save report to file")
    args = parser.parse_args()

    entries = parse_log(args.log)
    results = analyse(entries)
    print_report(results, args.log)

    if args.report:
        save_report(results, args.log)
