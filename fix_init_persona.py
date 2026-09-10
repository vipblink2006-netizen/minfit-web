with open('database.py', 'r') as f:
    content = f.read()

content = content.replace(
    'def load_persona_weights_from_database() -> dict[str, dict[str, Decimal]]:\n    server, database_name, _ = settings()',
    'def load_persona_weights_from_database() -> dict[str, dict[str, Decimal]]:\n    ensure_database()\n    server, database_name, _ = settings()'
)

with open('database.py', 'w') as f:
    f.write(content)
