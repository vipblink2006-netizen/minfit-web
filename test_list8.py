from database import connect, to_dict
with connect() as conn:
    rows = conn.execute("SELECT id, name, is_global, broker_id, is_active FROM Projects WHERE name = 'Test Broker Project'").fetchall()
    for r in rows:
        d = to_dict(r)
        print("broker_id:", repr(d["broker_id"]))
