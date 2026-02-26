import csv
import json
from datetime import datetime, timedelta
import ipaddress
from collections import defaultdict

LOG_FILE = "../frontend/data/sample_logs_no_status.csv"
TIME_WINDOW = timedelta(minutes=5)
BRUTE_FORCE_THRESHOLD = 5

def is_internal_ip(ip):
    internal_ranges = [
        ipaddress.ip_network("192.168.0.0/16"),
        ipaddress.ip_network("10.0.0.0/8"),
        ipaddress.ip_network("172.16.0.0/12"),
    ]
    ip_obj = ipaddress.ip_address(ip)
    return any(ip_obj in net for net in internal_ranges)

def parse_logs():
    logs = []
    with open(LOG_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["timestamp"] = datetime.fromisoformat(row["timestamp"])
            logs.append(row)
    return sorted(logs, key=lambda x: x["timestamp"])

def detect_bruteforce(logs):
    anomalies = []
    ip_events = defaultdict(list)

    for log in logs:
        if log["action"] == "login_failed":
            ip_events[log["ip_address"]].append(log)

    for ip, events in ip_events.items():
        for i in range(len(events)):
            window = [
                e for e in events
                if events[i]["timestamp"] <= e["timestamp"] <= events[i]["timestamp"] + TIME_WINDOW
            ]
            if len(window) >= BRUTE_FORCE_THRESHOLD:
                anomalies.append({
                    "timestamp": events[i]["timestamp"].isoformat(),
                    "user_id": events[i]["user_id"],
                    "ip_address": ip,
                    "reason": f"Brute force suspected ({len(window)} failed logins in 5 minutes)"
                })
                break
    return anomalies

def detect_external_ip(logs):
    anomalies = []
    for log in logs:
        if not is_internal_ip(log["ip_address"]):
            anomalies.append({
                "timestamp": log["timestamp"].isoformat(),
                "user_id": log["user_id"],
                "ip_address": log["ip_address"],
                "reason": "Access from external/public IP"
            })
    return anomalies

def detect_geo_hop(logs):
    anomalies = []
    user_events = defaultdict(list)

    for log in logs:
        if log["action"] == "login_success":
            user_events[log["user_id"]].append(log)

    for user, events in user_events.items():
        for i in range(len(events) - 1):
            time_diff = events[i+1]["timestamp"] - events[i]["timestamp"]
            if time_diff <= TIME_WINDOW and events[i]["ip_address"] != events[i+1]["ip_address"]:
                anomalies.append({
                    "timestamp": events[i+1]["timestamp"].isoformat(),
                    "user_id": user,
                    "ip_address": events[i+1]["ip_address"],
                    "reason": "Geo-hop suspected (login from different IP within short time)"
                })
    return anomalies

def main():
    logs = parse_logs()

    anomalies = []
    anomalies.extend(detect_bruteforce(logs))
    anomalies.extend(detect_external_ip(logs))
    anomalies.extend(detect_geo_hop(logs))

    with open("anomaly_report.json", "w") as f:
        json.dump(anomalies, f, indent=4)

    print(f"Detected {len(anomalies)} anomalies.")
    print("Report saved to anomaly_report.json")

if __name__ == "__main__":
    main()