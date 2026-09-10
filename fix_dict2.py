with open('database.py', 'r') as f:
    content = f.read()

# Remove the broken function
import re
content = re.sub(r'def row_to_row_to_dict\(row\):\n    if hasattr\(row, "_asdict"\):\n        return row\._asdict\(\)\n    return row_to_dict\(row\)\n', '', content)

# Add the correct function at the top
helper = """
def row_to_dict_helper(row):
    if hasattr(row, "_asdict"):
        return row._asdict()
    from collections import namedtuple
    if hasattr(row, "_fields"): return dict(zip(row._fields, row))
    return dict(row)
"""

content = content.replace('import sqlite3', 'import sqlite3\n' + helper)

# Replace all row_to_dict with row_to_dict_helper
content = content.replace("row_to_dict", "row_to_dict_helper")

with open('database.py', 'w') as f:
    f.write(content)
