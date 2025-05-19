import time, json, hashlib, requests
import platform
from system_checks import run_all_checks

LAST_HASH = ""

def hash_data(data):
    return hashlib.md5(json.dumps(data, sort_keys=True).encode()).hexdigest()

def send_to_server(data):
    data['machine_id'] = platform.node()
    data['os'] = platform.system()
    try:
        requests.post("http://127.0.0.1:8000/report", json=data)
    except Exception as e:
        print("Failed to send:", e)

def run_daemon():
    global LAST_HASH
    while True:
        data = run_all_checks()
        current_hash = hash_data(data)
        if current_hash != LAST_HASH:
            send_to_server(data)
            LAST_HASH = current_hash
        time.sleep(1800)  # Run every 30 minutes

if __name__ == "__main__":
    run_daemon()