with open('database.py', 'r') as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if line.startswith('def to_to_dict(row):') or line.startswith('def row_to_row_to_dict(row):') or line.startswith('def row_to_dict_helper(row):') or line.startswith('def row_to_dict(row):') or line.startswith('def to_dict(row):'):
        skip = True
    
    if skip:
        if line.strip() == 'return dict(row)' or line.strip() == 'return to_dict(row)' or line.strip() == 'return row_to_dict(row)' or line.strip() == 'return row_to_dict_helper(row)':
            skip = False
            continue
        continue

    new_lines.append(line)

content = "".join(new_lines)

# Inject to_dict cleanly
helper = """
def to_dict(row):
    if hasattr(row, "_asdict"):
        return row._asdict()
    if hasattr(row, "_fields"): 
        return dict(zip(row._fields, row))
    return dict(row)
"""

content = content.replace("import sqlite3\n", "import sqlite3\n" + helper)

with open('database.py', 'w') as f:
    f.write(content)
