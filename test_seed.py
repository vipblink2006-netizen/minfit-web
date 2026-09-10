import database
try:
    with database.connect(autocommit=True) as conn:
        database._ensure_users_table_and_seeds(conn)
        print("Seed success!")
except Exception as e:
    import traceback
    traceback.print_exc()
