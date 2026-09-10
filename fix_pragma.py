import re

with open('database.py', 'r') as f:
    content = f.read()

# Replace the PRAGMA block
pragma_block = """    cols = [r[1] for r in connection.execute("PRAGMA table_info(Users)").fetchall()]
    if "units_sold" not in cols:
        connection.execute("ALTER TABLE Users ADD COLUMN units_sold INTEGER DEFAULT 0")
    if "clients_count" not in cols:
        connection.execute("ALTER TABLE Users ADD COLUMN clients_count INTEGER DEFAULT 0")
    if "projects_count" not in cols:
        connection.execute("ALTER TABLE Users ADD COLUMN projects_count INTEGER DEFAULT 0")
    if "password_hash" not in cols:
        connection.execute("ALTER TABLE Users ADD COLUMN password_hash TEXT DEFAULT ''")"""

new_pragma_block = """    try:
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

content = content.replace(pragma_block, new_pragma_block)

# Also fix INSERT OR IGNORE since _convert_query replaces it with INSERT INTO DO NOTHING, which might fail on sqlite if not using DO NOTHING. Wait, SQLite supports INSERT OR IGNORE natively. Postgres needs ON CONFLICT.
# Actually I already replaced it globally in convert_query.

with open('database.py', 'w') as f:
    f.write(content)
