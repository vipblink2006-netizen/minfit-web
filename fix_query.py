with open('database.py', 'r') as f:
    content = f.read()

# Fix the regex replacement for INSERT OR IGNORE
content = content.replace(
    r"q = re.sub(r'\bINSERT OR IGNORE INTO\b', 'INSERT INTO', q, flags=re.IGNORECASE)",
    r"q = re.sub(r'\bINSERT OR IGNORE INTO\b', 'INSERT INTO', q, flags=re.IGNORECASE)"
)

# Actually, the simplest fix is to just remove the regex and handle it specifically for Users:
# Wait, let's just rewrite the convert_query part completely.
import re

def rewrite(match):
    return ""

new_code = """
    # Simple patches for SQLite to Postgres
    
    if "INSERT OR IGNORE INTO Users" in q:
        q = q.replace("INSERT OR IGNORE INTO", "INSERT INTO")
        q += " ON CONFLICT (id) DO NOTHING"
    else:
        q = re.sub(r'\\bINSERT OR IGNORE INTO\\b', 'INSERT INTO', q, flags=re.IGNORECASE)

"""

content = content.replace(
    "    q = re.sub(r'\\bINSERT OR IGNORE INTO\\b', 'INSERT INTO', q, flags=re.IGNORECASE)",
    new_code
)

# And remove the duplicate check at the end
content = content.replace(
    """    if "INSERT OR IGNORE INTO Users" in q:
        q = q.replace("INSERT OR IGNORE INTO", "INSERT INTO") + " ON CONFLICT (id) DO NOTHING\"""",
    ""
)

with open('database.py', 'w') as f:
    f.write(content)
