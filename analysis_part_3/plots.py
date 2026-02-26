import pandas as pd
import numpy as np
import ipaddress
import matplotlib.pyplot as plt

CSV_PATH = "../frontend/data/sample_logs_no_status.csv"  # תעדכן לשם אצלך

private_nets = [
    ipaddress.ip_network("10.0.0.0/8"),
    ipaddress.ip_network("172.16.0.0/12"),
    ipaddress.ip_network("192.168.0.0/16"),
]

def is_private(ip: str) -> bool:
    try:
        addr = ipaddress.ip_address(ip)
        return any(addr in n for n in private_nets)
    except ValueError:
        return False

df = pd.read_csv(CSV_PATH)
df["timestamp"] = pd.to_datetime(df["timestamp"])
df = df.sort_values("timestamp")

df["is_private"] = df["ip_address"].apply(is_private)
df["is_login_fail"] = df["action"].eq("login_failed")

# 1) Timeline: login_failed per 5 minutes
ts_fail = df[df["is_login_fail"]].set_index("timestamp").resample("5min").size()
plt.figure()
plt.plot(ts_fail.index, ts_fail.values, marker="o", linestyle="-")
plt.title("login_failed events per 5 minutes")
plt.xlabel("time")
plt.ylabel("count")
plt.tight_layout()
plt.savefig("bonus1_login_failed_timeline.png", dpi=160)
plt.close()

# 2) Top public IPs
external_df = df[~df["is_private"]]
top_ext = external_df["ip_address"].value_counts().head(15)
plt.figure(figsize=(8,4))
plt.bar(top_ext.index, top_ext.values)
plt.title("Top public IPs by activity count")
plt.xlabel("ip_address")
plt.ylabel("events")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("bonus1_top_public_ips.png", dpi=160)
plt.close()

# 3) Heatmap: failed logins by user and hour
heat = df[df["is_login_fail"]].copy()
heat["hour"] = heat["timestamp"].dt.hour
pivot = heat.pivot_table(index="user_id", columns="hour", values="action",
                         aggfunc="count", fill_value=0)
pivot["total"] = pivot.sum(axis=1)
pivot = pivot.sort_values("total", ascending=False).head(20).drop(columns=["total"])

plt.figure(figsize=(10,6))
plt.imshow(pivot.values, aspect="auto")
plt.title("Top users: login_failed count by hour-of-day (heatmap)")
plt.xlabel("hour")
plt.ylabel("user_id (top 20)")
plt.xticks(ticks=np.arange(len(pivot.columns)), labels=pivot.columns)
plt.yticks(ticks=np.arange(len(pivot.index)), labels=pivot.index)
plt.colorbar(label="failed logins")
plt.tight_layout()
plt.savefig("bonus1_failed_login_heatmap.png", dpi=160)
plt.close()

print("Saved: bonus1_login_failed_timeline.png, bonus1_top_public_ips.png, bonus1_failed_login_heatmap.png")