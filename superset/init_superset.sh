#!/bin/bash
set -e

echo "=============================="
echo "Starting Superset Init"
echo "=============================="

echo "Upgrading database..."
superset db upgrade

echo "Creating admin user..."
superset fab create-admin \
  --username admin \
  --firstname admin \
  --lastname admin \
  --email admin@test.com \
  --password admin || true

echo "Initializing Superset..."
superset init


echo "Starting Superset..."
superset run -h 0.0.0.0 -p 8088 &
SUPERSET_PID=$!

echo "Waiting for Superset health..."
until curl -s http://localhost:8088/health >/dev/null; do
  echo "waiting..."
  sleep 2
done

echo "Superset is ready"


echo "======================================"
echo "IMPORTANT MANUAL STEP REQUIRED:"
echo "Create ClickHouse database in UI"
echo "Settings → Database → + Database"
echo "======================================"

echo "Waiting for ClickHouse database (Superset metadata)..."

python3 - <<'EOF'
import requests
import time
import glob
import os

url = "http://localhost:8088/api/v1/database/"

login_payload = {
    "username": "admin",
    "password": "admin",
    "provider": "db",
    "refresh": True
    }

def has_clickhouse():

    r = requests.post("http://localhost:8088/api/v1/security/login",json=login_payload)
    access_token = r.json()["access_token"]

    payload = {}
    headers = {
      'Accept': 'application/json',
      'Authorization': "Bearer " + access_token
    }

    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code != 200:
            return False
        data = response.json()
        names = data['result'][0]['backend']
        return "clickhousedb" in names or "ClickHouse" in names
    except Exception:
        return False

while not has_clickhouse():
    print("waiting for ClickHouse connection...")
    time.sleep(7)

print("ClickHouse connection detected!")


print("Uploadin dashboards")
BASE = "http://localhost:8088"
session = requests.Session()

login = session.post(f"{BASE}/api/v1/security/login", json=login_payload)
token = login.json()["access_token"]

session.headers.update({
    "Authorization": f"Bearer {token}"
})

# 2. CSRF
csrf = session.get(f"{BASE}/api/v1/security/csrf_token/")
session.headers.update({
    "X-CSRFToken": csrf.json()["result"],
    "Referer": BASE
})

# 3. Upload dashboard zip
for zip_path in glob.glob("/app/superset/dashboards/*.zip"):
    print(f"Importing {os.path.basename(zip_path)}...")
    
    with open(zip_path, "rb") as f:
        resp = session.post(
            f"{BASE}/api/v1/dashboard/import/",
            files={"formData": ( os.path.basename(zip_path),f,"application/zip",)},
            data={
                "overwrite": "true",
                "passwords": "{\"databases/Other.yaml\": \"default123\"}"
            }
        )
    print(f"Status: {resp.status_code}")
    print(resp.text)
    resp.raise_for_status()


EOF

echo "Superset fully initialized"

wait $SUPERSET_PID