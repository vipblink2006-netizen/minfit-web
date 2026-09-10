from database import connect, to_dict
broker_id = "brk_moigioi"
condition = "WHERE 1=1 AND p.is_active = 1"
condition += " AND (p.is_global = 1 OR p.broker_id = ?)"
params = [broker_id]
query = f"""
        SELECT p.*, pa.amenity_code
        FROM Projects AS p
        LEFT JOIN ProjectAmenities AS pa ON pa.project_id = p.id
        {condition}
        ORDER BY p.is_global DESC, p.created_at DESC, p.id, pa.amenity_code;
        """
with connect() as conn:
    rows = conn.execute(query, params).fetchall()
    found = False
    for r in rows:
        d = to_dict(r)
        if d["id"] == 'prj_0_1700':
            print("FOUND WITH QUERY!")
            found = True
    if not found:
        print("NOT FOUND WITH QUERY!")
