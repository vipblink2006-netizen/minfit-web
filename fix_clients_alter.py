with open('workflow_api.py', 'r') as f:
    content = f.read()

import re
new_func = """
def _ensure_workflow_tables() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    from database import settings
    server, _, _ = settings()
    is_postgres = server.lower() in ("postgres", "supabase")
    
    with connect() as connection:
        if is_postgres:
            connection.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id SERIAL PRIMARY KEY,
                broker_id TEXT DEFAULT 'broker_default',
                name TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                status TEXT NOT NULL DEFAULT 'saved',
                profile_json TEXT,
                units_sold INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            ''')
            connection.commit()
        else:
            connection.executescript('''
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                broker_id TEXT DEFAULT 'broker_default',
                name TEXT NOT NULL,
                email TEXT,
                phone TEXT,
                status TEXT NOT NULL DEFAULT 'saved',
                profile_json TEXT,
                units_sold INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
            ''')
            try:
                connection.execute("ALTER TABLE clients ADD COLUMN broker_id TEXT DEFAULT 'broker_default'")
            except Exception:
                pass
            try:
                connection.execute("ALTER TABLE clients ADD COLUMN units_sold INTEGER DEFAULT 0")
            except Exception:
                pass
            connection.commit()
"""

# Replace the old function
content = re.sub(r'def _ensure_workflow_tables\(\) -> None:.*?(?=\n\ndef )', new_func.strip(), content, flags=re.DOTALL)

with open('workflow_api.py', 'w') as f:
    f.write(content)
