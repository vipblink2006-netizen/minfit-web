with open('database.py', 'r') as f:
    content = f.read()

import re
# Remove all my helper garbage
content = re.sub(r'def row_to_.*?\n    return dict\(row\)\n', '', content, flags=re.DOTALL)
content = re.sub(r'def row_to_.*?\n    return row_to_dict_helper\(row\)\n', '', content, flags=re.DOTALL)
content = re.sub(r'def row_to_dict_helper_helper\(row\):.*?\n    return dict\(row\)\n', '', content, flags=re.DOTALL)

# Also remove row_to_dict(row) everywhere, revert to dict(row)
content = re.sub(r'row_to_dict_helper\(', 'dict(', content)
content = re.sub(r'row_to_dict\(', 'dict(', content)
content = re.sub(r'row_to_row_to_dict\(', 'dict(', content)

# Now inject cleanly
helper = """
def to_dict(row):
    if hasattr(row, "_asdict"):
        return row._asdict()
    if hasattr(row, "_fields"): 
        return dict(zip(row._fields, row))
    return dict(row)
"""

content = content.replace("import sqlite3\n", "import sqlite3\n" + helper)

# Safely replace dict(...) with to_dict(...)
# Only replace specific dict(x) calls, NOT "dict(" generally to avoid hitting to_dict
content = content.replace("dict(row)", "to_dict(row)")
content = content.replace("dict(ur)", "to_dict(ur)")
content = content.replace("dict(cr)", "to_dict(cr)")
content = content.replace("dict(r)", "to_dict(r)")

with open('database.py', 'w') as f:
    f.write(content)
