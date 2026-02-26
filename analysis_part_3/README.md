# 🔐 Task 3 — Login Anomaly Detection & Security Analysis  
### RSecurity Dashboard – analysis_part_3

This module analyzes authentication logs and detects suspicious login behavior using rule-based logic and statistical methods.

It produces:
- 📄 `anomaly_report.json` — structured anomaly report (with severity + mitigation)
- 📊 Bonus visualizations (PNG files)
- 🤖 Algorithmic anomaly detection (3-sigma statistical model)

------------------------------------------------------------------------

# 📁 Project Structure
RSecurity-Dashboard/
└── analysis_part_3/
├── analyze_logs.py
├── plots.py
├── anomaly_report.json
├── bonus1_failed_login_heatmap.png
├── bonus1_top_public_ips.png
└── venv/


-----------------------------------------------------------------------

# 📥 Input Data

The system analyzes:
frontend/data/sample_logs_no_status.csv


Expected CSV fields:

- `timestamp`
- `user_id`
- `ip_address`
- `action` (`login_success` / `login_failed`)

----------------------------------------------------------------

# 🚀 How to Run

### 1️⃣ Activate virtual environment
```bash
cd analysis_part_3
python -m venv venv
venv\Scripts\activate   # Windows

2️⃣ Install dependencies
pip install numpy pandas matplotlib

3️⃣ Run anomaly detection

python analyze_logs.py

4️⃣ Run visualizations (Bonus 1)
python plots.py

--------------------------------------------------------------------------------


🔎 Detection Logic
1️⃣ Brute Force Detection 🔥

Detects repeated failed login attempts from the same IP within a 5-minute window.

Condition:

≥ 5 login_failed events

Same IP

Within 5 minutes

Severity: high
Mitigation:

Block IP temporarily

Alert SOC/admin

Enable account lockout

Enforce MFA

------------------------------------------------------------------

2️⃣ External/Public IP Activity 🌍

Identifies access from non-private IP ranges.

Private ranges:

10.0.0.0/8

172.16.0.0/12

192.168.0.0/16

Instead of flagging every event, IPs are grouped:

Output includes:

first_seen

last_seen

total_events

unique_users

Severity: medium
Mitigation:

Verify VPN/remote access

Alert admin

Enforce MFA

--------------------------------------------------------------------

3️⃣ Geo-Hop Detection ✈️

Detects impossible travel behavior:

Same user

Two successful logins

Different IPs

Within 5 minutes

Severity: high
Mitigation:

Force MFA challenge

Invalidate sessions

Notify user + admin
----------------------------------------------------------------------------

🤖 Bonus 3 — Algorithmic Anomaly Detection (3-Sigma Rule)

This module implements statistical outlier detection:

Method:

Count events per IP.

Compute:

Mean activity

Standard deviation

Define threshold:

threshold = mean + 3 * std

Flag IPs exceeding threshold.

This is based on the 3-sigma statistical rule, commonly used in anomaly detection.

Example output:
Statistical anomaly: unusually high activity (22 events vs avg 3.13, threshold 13.01)

Severity: medium
Mitigation:

Investigate activity spike

Check threat intelligence

Correlate with failed logins

Apply rate limiting if needed
----------------------------------------------------------------------

📄 Output Format (anomaly_report.json)

Each anomaly contains:

{
  "timestamp": "...",
  "user_id": "...",
  "ip_address": "...",
  "reason": "...",
  "severity": "low | medium | high",
  "mitigation": [ ... ],
  "first_seen": "...",
  "last_seen": "...",
  "total_events": 0,
  "unique_users": []
}

-------------------------------------------------------------
📊 Bonus 1 — Visualizations

Generated via plots.py:

📈 1) Login Failures Timeline

5-minute resampled counts

Helps identify brute-force spikes

🌐 2) Top Public IPs by Activity

Bar chart of most active external IPs

🔥 3) Heatmap — Failed Logins by User & Hour

Shows suspicious login patterns by time-of-day

Highlights potential targeted attacks
---------------------------------------------------------------------------
🧠 Security Design Considerations

✔ Noise reduction by grouping external IPs
✔ Severity classification
✔ Structured mitigation guidance
✔ Combination of rule-based + statistical detection
✔ Ready for extension to ML models (Isolation Forest, clustering, etc.)


🏆 Bonus Coverage

| Feature                           | Implemented                   |
| --------------------------------- | ----------------------------- |
| Bonus 1 — Visualizations          | ✅                             |
| Bonus 2 — Mitigation Suggestions  | ✅                             |
| Bonus 3 — Algorithmic / ML Method | ✅ (3-sigma statistical model) |


