with open('database.py', 'r') as f:
    content = f.read()

content = content.replace(
    'if server.lower() == "sqlite":\n        _sqlite_ready(database_name)\n        weights',
    'if server.lower() in ("sqlite", "postgres", "supabase"):\n        if server.lower() == "sqlite":\n            _sqlite_ready(database_name)\n        weights'
)

with open('database.py', 'w') as f:
    f.write(content)
