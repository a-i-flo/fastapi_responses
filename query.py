import requests

BASE = "http://127.0.0.1:8001"


# Get a specific rat
r = requests.get(f"{BASE}/rats/rat1")
r.raise_for_status()
rat = r.json()
print(rat["ratnumber"], rat["group"], rat["responses"])


# Daily averages
r = requests.get(f"{BASE}/daily/average")
r.raise_for_status()
avg = r.json()

for row in avg["rows"]:
    print(row["day"], row["lever_mean"], row["nosepokes_mean"])

