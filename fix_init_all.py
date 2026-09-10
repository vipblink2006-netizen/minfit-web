with open('database.py', 'r') as f:
    content = f.read()

import re
# Find ensure_database()
new_func = """
def ensure_database() -> None:
    try:
        from database import settings
        server, db_url, _ = settings()
        if server.lower() in ("postgres", "supabase"):
            _ensure_postgres_database()
        else:
            _sqlite_ready("database.db")
            with sqlite3.connect("database.db") as conn:
                _ensure_sqlite_database(conn)
                _ensure_users_table_and_seeds(conn)
        
        # Ensure workflow tables are created too!
        import workflow_api
        workflow_api._ensure_workflow_tables()
        print("Database initialized successfully.")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print("Lỗi khởi tạo DB:", e)
"""

content = re.sub(r'def ensure_database\(\) -> None:.*?(?=\n\nif __name__)', new_func.strip(), content, flags=re.DOTALL)

# But wait, we should also call it in list_users_from_db just to be absolutely safe!
content = content.replace("def list_users_from_db() -> list[dict[str, Any]]:\n    with connect() as connection:", "def list_users_from_db() -> list[dict[str, Any]]:\n    import workflow_api\n    workflow_api._ensure_workflow_tables()\n    with connect() as connection:")

with open('database.py', 'w') as f:
    f.write(content)
