with open('database.py', 'r') as f:
    content = f.read()

# Add row_to_dict function
helper = """
def row_to_dict(row):
    if hasattr(row, "_asdict"):
        return row._asdict()
    return dict(row)
"""

if "def row_to_dict" not in content:
    content = content.replace("import sqlite3\n", "import sqlite3\n" + helper)

# Replace dict(row) calls
content = content.replace("dict(row)", "row_to_dict(row)")
content = content.replace("dict(ur)", "row_to_dict(ur)")
content = content.replace("dict(cr)", "row_to_dict(cr)")
content = content.replace("dict(r)", "row_to_dict(r)")

with open('database.py', 'w') as f:
    f.write(content)
