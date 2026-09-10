with open('database.py', 'r') as f:
    content = f.read()

content = content.replace("def get_user_stats_from_db() -> dict[str, Any]:\n    with connect() as connection:", "def get_user_stats_from_db() -> dict[str, Any]:\n    import workflow_api\n    workflow_api._ensure_workflow_tables()\n    with connect() as connection:")

with open('database.py', 'w') as f:
    f.write(content)
