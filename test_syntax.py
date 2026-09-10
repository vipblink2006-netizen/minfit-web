import database
try:
    with database.connect(autocommit=True) as conn:
        conn.executescript("CREATE TABLE IF NOT EXISTS test_auto (id INTEGER PRIMARY KEY AUTOINCREMENT)")
except Exception as e:
    print(repr(e))
