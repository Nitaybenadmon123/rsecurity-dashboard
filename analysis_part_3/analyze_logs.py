import csv
import json
from datetime import datetime, timedelta
import ipaddress
from collections import defaultdict, Counter
from typing import List, Dict, Any, Tuple
import numpy as np

LOG_FILE = "../frontend/data/sample_logs_no_status.csv"
TIME_WINDOW = timedelta(minutes=5)
BRUTE_FORCE_THRESHOLD = 5


# ---------- helpers ----------
def is_internal_ip(ip: str) -> bool:
    internal_ranges = [
        ipaddress.ip_network("10.0.0.0/8"),
        ipaddress.ip_network("172.16.0.0/12"),
        ipaddress.ip_network("192.168.0.0/16"),
    ]
    try:
        ip_obj = ipaddress.ip_address(ip)
    except ValueError:
        return False
    return any(ip_obj in net for net in internal_ranges)


def suggest_mitigation(reason: str, is_internal: bool) -> Tuple[str, List[str]]:
    r = reason.lower()

    # 1) Brute force
    if "brute" in r:
        return "high", [
            "Temporarily block the IP (30-60 minutes) or apply rate limiting",
            "Alert admin/SOC about brute-force attempt",
            "Enable account lockout / CAPTCHA after repeated failures",
            "Require MFA for the affected account(s)",
        ]

    # 2) Geo-hop
    if "geo" in r or "hop" in r or "impossible" in r:
        return "high", [
            "Force MFA challenge and re-authentication",
            "Invalidate active sessions / revoke tokens",
            "Notify user and admin about suspicious login pattern",
        ]

    # 3) Statistical anomaly (bonus 3)
    if "statistical anomaly" in r or "outlier" in r:
        return "medium", [
            "Investigate unusual spike in activity",
            "Check IP reputation / threat intelligence",
            "Correlate with failed logins or multiple users",
            "Consider temporary rate limiting if activity persists",
        ]

    # 4) External/public IP (only if this is the reason)
    if "external" in r or "public ip" in r:
        return "medium", [
            "Verify if the IP is expected (VPN/remote); otherwise block or challenge",
            "Alert admin/SOC about off-network activity",
            "Enforce MFA / conditional access for off-network logins",
        ]

    # fallback
    return "low", ["Log and monitor; review manually if it repeats"]


def enrich_anomaly(a: Dict[str, Any]) -> Dict[str, Any]:
    internal = is_internal_ip(a.get("ip_address", ""))
    severity, mitigation = suggest_mitigation(a.get("reason", ""), internal)
    a["severity"] = severity
    a["mitigation"] = mitigation
    return a


def parse_logs() -> List[Dict[str, Any]]:
    logs: List[Dict[str, Any]] = []
    with open(LOG_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["timestamp"] = datetime.fromisoformat(row["timestamp"])
            logs.append(row)
    return sorted(logs, key=lambda x: x["timestamp"])


# ---------- detectors ----------
def detect_bruteforce(logs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    anomalies = []
    ip_events = defaultdict(list)

    for log in logs:
        if log["action"] == "login_failed":
            ip_events[log["ip_address"]].append(log)

    for ip, events in ip_events.items():
        events = sorted(events, key=lambda x: x["timestamp"])

        for i in range(len(events)):
            start_ts = events[i]["timestamp"]
            end_ts = start_ts + TIME_WINDOW

            count = 0
            for e in events[i:]:
                if e["timestamp"] > end_ts:
                    break
                count += 1

            if count >= BRUTE_FORCE_THRESHOLD:
                anomalies.append(enrich_anomaly({
                    "timestamp": start_ts.isoformat(),
                    "user_id": events[i]["user_id"],
                    "ip_address": ip,
                    "reason": f"Brute force suspected ({count} failed logins in {int(TIME_WINDOW.total_seconds()//60)} minutes)"
                }))
                break

    return anomalies


def detect_external_ip_grouped(logs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Instead of reporting EVERY external event, group by IP to avoid noisy reports.
    """
    anomalies = []
    by_ip = defaultdict(list)

    for log in logs:
        ip = log["ip_address"]
        if not is_internal_ip(ip):
            by_ip[ip].append(log)

    for ip, events in by_ip.items():
        events = sorted(events, key=lambda x: x["timestamp"])
        users = sorted({e["user_id"] for e in events})
        total = len(events)

        reason = f"Access from external/public IP ({total} events, {len(users)} users)"

        anomalies.append(enrich_anomaly({
            "timestamp": events[0]["timestamp"].isoformat(),
            "user_id": "multiple" if len(users) > 1 else users[0],
            "ip_address": ip,
            "reason": reason,
            "first_seen": events[0]["timestamp"].isoformat(),
            "last_seen": events[-1]["timestamp"].isoformat(),
            "total_events": total,
            "unique_users": users,
        }))

    return anomalies


def detect_geo_hop(logs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    anomalies = []
    user_events = defaultdict(list)

    for log in logs:
        if log["action"] == "login_success":
            user_events[log["user_id"]].append(log)

    for user, events in user_events.items():
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


def detect_statistical_outliers(logs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Bonus 3: algorithmic anomaly detection using 3-sigma rule (mean + 3*std)
    over activity counts per IP.
    """
    anomalies = []

    by_ip = defaultdict(list)
    for log in logs:
        by_ip[log["ip_address"]].append(log)

    ip_counts = {ip: len(events) for ip, events in by_ip.items()}
    values = np.array(list(ip_counts.values()), dtype=float)

    mean = values.mean()
    std = values.std()
    threshold = mean + 3 * std

    for ip, count in ip_counts.items():
        if count > threshold:
            events = sorted(by_ip[ip], key=lambda x: x["timestamp"])
            users = sorted({e["user_id"] for e in events})

            anomalies.append(enrich_anomaly({
                "timestamp": events[0]["timestamp"].isoformat(),
                "user_id": "multiple" if len(users) > 1 else users[0],
                "ip_address": ip,
                "reason": f"Statistical anomaly: unusually high activity ({count} events vs avg {mean:.2f}, threshold {threshold:.2f})",
                "first_seen": events[0]["timestamp"].isoformat(),
                "last_seen": events[-1]["timestamp"].isoformat(),
                "total_events": count,
                "unique_users": users,
            }))

    return anomalies


# ---------- main ----------
def main():
    logs = parse_logs()

    anomalies: List[Dict[str, Any]] = []
    anomalies.extend(detect_bruteforce(logs))
    anomalies.extend(detect_external_ip_grouped(logs))   # grouped, less noise
    anomalies.extend(detect_geo_hop(logs))
    anomalies.extend(detect_statistical_outliers(logs))  # bonus 3

    with open("anomaly_report.json", "w", encoding="utf-8") as f:
        json.dump(anomalies, f, indent=4)

    print(f"Detected {len(anomalies)} anomalies.")
    print("Report saved to anomaly_report.json")


if __name__ == "__main__":
    main()