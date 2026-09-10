from database import connect, to_dict
with connect() as conn:
    rows = conn.execute("SELECT id, name, is_global, broker_id, is_active FROM Projects WHERE name = 'Test Broker Project'").fetchall()
    for r in rows:
        print(to_dict(r))
