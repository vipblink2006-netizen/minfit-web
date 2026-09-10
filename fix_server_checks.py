with open('database.py', 'r') as f:
    content = f.read()

# Fix load_projects_from_database
content = content.replace(
    'if server.lower() == "sqlite":\n        _sqlite_ready(database_name)\n        condition = "WHERE 1=1"',
    'if server.lower() in ("sqlite", "postgres", "supabase"):\n        if server.lower() == "sqlite":\n            _sqlite_ready(database_name)\n        condition = "WHERE 1=1"'
)

# Fix load_persona_weights_from_database
content = content.replace(
    'if server.lower() == "sqlite":\n        _sqlite_ready(database_name)\n        with connect() as connection:',
    'if server.lower() in ("sqlite", "postgres", "supabase"):\n        if server.lower() == "sqlite":\n            _sqlite_ready(database_name)\n        with connect() as connection:'
)

# Fix database_status
content = content.replace(
    'if server.lower() == "sqlite":\n        _sqlite_ready(database_name)\n        return _sqlite_status(database_name)',
    'if server.lower() in ("sqlite", "postgres", "supabase"):\n        if server.lower() == "sqlite":\n            _sqlite_ready(database_name)\n        return _sqlite_status(database_name) # Will use _sqlite_status temporarily for postgres'
)

with open('database.py', 'w') as f:
    f.write(content)
