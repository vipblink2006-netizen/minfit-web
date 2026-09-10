with open('workflow_api.py', 'r') as f:
    content = f.read()

old_val1 = "        val1 = float(val1_str.replace(\",\", \".\")) if val1_str else 0\n        if has_x1: val1 += 5"
new_val1 = "        val1 = float(val1_str.replace(\",\", \".\")) if val1_str else 0\n        if has_x1:\n            if val1 < 10: val1 = val1 * 10 + 5\n            else: val1 += 5"

old_val2 = "            val2 = float(val2_str.replace(\",\", \".\"))\n            if has_x2: val2 += 5"
new_val2 = "            val2 = float(val2_str.replace(\",\", \".\"))\n            if has_x2:\n                if val2 < 10: val2 = val2 * 10 + 5\n                else: val2 += 5"

content = content.replace(old_val1, new_val1).replace(old_val2, new_val2)

with open('workflow_api.py', 'w') as f:
    f.write(content)
