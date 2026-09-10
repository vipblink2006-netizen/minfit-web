with open('database.py', 'r') as f:
    content = f.read()

# Replace the try-except PRAGMA block to avoid breaking Postgres transactions
old_block = """    try:
        cols = [r[1] for r in connection.execute("PRAGMA table_info(Users)").fetchall()]
        if "units_sold" not in cols:
            connection.execute("ALTER TABLE Users ADD COLUMN units_sold INTEGER DEFAULT 0")
        if "clients_count" not in cols:
            connection.execute("ALTER TABLE Users ADD COLUMN clients_count INTEGER DEFAULT 0")
        if "projects_count" not in cols:
            connection.execute("ALTER TABLE Users ADD COLUMN projects_count INTEGER DEFAULT 0")
        if "password_hash" not in cols:
            connection.execute("ALTER TABLE Users ADD COLUMN password_hash TEXT DEFAULT ''")
    except Exception:
        pass  # Postgres schema is already up to date"""

new_block = """    server, _, _ = settings()
    if server.lower() == 'sqlite':
        try:
            cols = [r[1] for r in connection.execute("PRAGMA table_info(Users)").fetchall()]
            if "units_sold" not in cols:
                connection.execute("ALTER TABLE Users ADD COLUMN units_sold INTEGER DEFAULT 0")
            if "clients_count" not in cols:
                connection.execute("ALTER TABLE Users ADD COLUMN clients_count INTEGER DEFAULT 0")
            if "projects_count" not in cols:
                connection.execute("ALTER TABLE Users ADD COLUMN projects_count INTEGER DEFAULT 0")
            if "password_hash" not in cols:
                connection.execute("ALTER TABLE Users ADD COLUMN password_hash TEXT DEFAULT ''")
        except Exception:
            pass"""

content = content.replace(old_block, new_block)

with open('database.py', 'w') as f:
    f.write(content)
