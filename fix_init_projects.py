with open('database.py', 'r') as f:
    content = f.read()

content = content.replace(
    'def load_projects_from_database(include_inactive: bool = False, broker_id: str | None = None) -> list[Project]:\n    server, database_name, _ = settings()',
    'def load_projects_from_database(include_inactive: bool = False, broker_id: str | None = None) -> list[Project]:\n    ensure_database()\n    server, database_name, _ = settings()'
)

with open('database.py', 'w') as f:
    f.write(content)
