import traceback
try:
    import database
    database.ensure_database()
except Exception:
    traceback.print_exc()
