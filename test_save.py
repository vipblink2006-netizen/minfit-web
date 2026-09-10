from workflow_api import create_or_update_project
from database import ensure_database, connect, to_dict

ensure_database()
payload = {
    "name": "Test Broker Project",
    "area": "Tây Hồ",
    "price_min_vnd": 5000000000,
    "area_m2": 70,
    "created_by_role": "broker",
    "broker_id": "brk_moigioi",
    "is_global": 0
}
res = create_or_update_project(payload)
pid = res["project_id"]

with connect() as conn:
    row = conn.execute("SELECT * FROM Projects WHERE id=?", (pid,)).fetchone()
    if row:
        print("FOUND RAW:", to_dict(row))
    else:
        print("RAW NOT FOUND!")
