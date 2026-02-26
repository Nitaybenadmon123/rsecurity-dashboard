import csv
import json
from datetime import datetime, timedelta
import ipaddress
from collections import defaultdict
from typing import Tuple, List, Dict, Any

LOG_FILE = "../frontend/data/sample_logs_no_status.csv"
TIME_WINDOW = timedelta(minutes=5)
BRUTE_FORCE_THRESHOLD = 5


def suggest_mitigation(reason: str, is_internal: bool):

    r = reason.lower()

    if "brute" in r:
        return "high", [
            "Temporarily block the IP (30-60 minutes)",
            "Alert admin/SOC about brute-force attempt",
            "Enable account lockout policy",
            "Require MFA for the affected account"
        ]

    if "geo" in r or "hop" in r:
        return "high", [
            "Force MFA challenge",
            "Invalidate active sessions",
            "Notify user and admin about suspicious travel"
        ]

  
    if "external" in r:
        return "medium", [
            "Verify if the IP is expected (VPN/remote); otherwise block or challenge",
            "Alert admin/SOC about off-network activity",
            "Enforce MFA / conditional access for off-network logins"
        ]

    return "low", ["Log and monitor"]

def is_internal_ip(ip: str) -> bool:
    internal_ranges = [
        ipaddress.ip_network("192.168.0.0/16"),
        ipaddress.ip_network("10.0.0.0/8"),
        ipaddress.ip_network("172.16.0.0/12"),
    ]
    try:
        ip_obj = ipaddress.ip_address(ip)
    except ValueError:
        return False
    return any(ip_obj in net for net in internal_ranges)


def parse_logs() -> List[Dict[str, Any]]:
    logs = []
    with open(LOG_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["timestamp"] = datetime.fromisoformat(row["timestamp"])
            logs.append(row)
    return sorted(logs, key=lambda x: x["timestamp"])


def enrich_anomaly(a: Dict[str, Any]) -> Dict[str, Any]:
    """
    Adds severity + mitigation based on reason and whether IP is internal.
    """
    internal = is_internal_ip(a.get("ip_address", ""))
    severity, mitigation = suggest_mitigation(a.get("reason", ""), internal)
    a["severity"] = severity
    a["mitigation"] = mitigation
    return a


def detect_bruteforce(logs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    anomalies = []
    ip_events = defaultdict(list)

    for log in logs:
        if log["action"] == "login_failed":
            ip_events[log["ip_address"]].append(log)

    for ip, events in ip_events.items():
        # events are already sorted globally; keep safe anyway
        events = sorted(events, key=lambda x: x["timestamp"])

        for i in range(len(events)):
            start_ts = events[i]["timestamp"]
            end_ts = start_ts + TIME_WINDOW

            # window count in [start_ts, end_ts]
            count = 0
            last_event = None
            for e in events[i:]:
                if e["timestamp"] > end_ts:
                    break
                count += 1
                last_event = e

            if count >= BRUTE_FORCE_THRESHOLD:
                anomalies.append(enrich_anomaly({
                    "timestamp": start_ts.isoformat(),
                    "user_id": events[i]["user_id"],
                    "ip_address": ip,
                    "reason": f"Brute force suspected ({count} failed logins in {int(TIME_WINDOW.total_seconds()//60)} minutes)"
                }))
                break

    return anomalies


def detect_external_ip(logs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    anomalies = []
    for log in logs:
        if not is_internal_ip(log["ip_address"]):
            anomalies.append(enrich_anomaly({
                "timestamp": log["timestamp"].isoformat(),
                "user_id": log["user_id"],
                "ip_address": log["ip_address"],
                "reason": "Access from external/public IP"
            }))
    return anomalies


def detect_geo_hop(logs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    anomalies = []
    user_events = defaultdict(list)

    # collect successful logins per user
    for log in logs:
        if log["action"] == "login_success":
            user_events[log["user_id"]].append(log)

    for user, events in user_events.items():
        # IMPORTANT: ensure time order per user
        events = sorted(events, key=lambda x: x["timestamp"])

        for i in range(len(events) - 1):
            a = events[i]
            b = events[i + 1]
            time_diff = b["timestamp"] - a["timestamp"]

            if time_diff <= TIME_WINDOW and a["ip_address"] != b["ip_address"]:
                anomalies.append(enrich_anomaly({
                    "timestamp": b["timestamp"].isoformat(),
                    "user_id": user,
                    "ip_address": b["ip_address"],
                    "reason": "Geo-hop suspected (login from different IP within short time)"
                }))

    return anomalies


def main():
    logs = parse_logs()

    anomalies = []
    anomalies.extend(detect_bruteforce(logs))
    anomalies.extend(detect_external_ip(logs))
    anomalies.extend(detect_geo_hop(logs))

    with open("anomaly_report.json", "w", encoding="utf-8") as f:
        json.dump(anomalies, f, indent=4)

    print(f"Detected {len(anomalies)} anomalies.")
    print("Report saved to anomaly_report.json")


if __name__ == "__main__":
    main()