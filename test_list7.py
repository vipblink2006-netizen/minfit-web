from database import connect, to_dict
with connect() as conn:
    rows = conn.execute("SELECT * FROM Projects WHERE broker_id = ?", ("brk_moigioi",)).fetchall()
    print("Found with ?, len:", len(rows))
    
    rows2 = conn.execute("SELECT * FROM Projects WHERE broker_id = 'brk_moigioi'").fetchall()
    print("Found with string, len:", len(rows2))

    rows3 = conn.execute("SELECT * FROM Projects WHERE is_global = 1 OR broker_id = ?", ("brk_moigioi",)).fetchall()
    print("Found with OR, len:", len(rows3))
