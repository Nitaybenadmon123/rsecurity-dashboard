import pandas as pd
import json

df = pd.read_csv("sample_logs_no_status.csv")

df = df.rename(columns={
    "user_id": "user",
    "ip_address": "ip"
})

df.insert(0, "id", range(1, len(df) + 1))

data = df.to_dict(orient="records")

with open("sampleData.json", "w") as f:
    json.dump(data, f, indent=2)

print("JSON file created successfully!")