with open('workflow_api.py', 'r') as f:
    content = f.read()

content = content.replace(
    "name_match = re.search(r'(?:dự án|project|khu căn hộ|tổ hợp)\\s*[:\\-–]?\\s*([^\\n\\r,;🔥🌟👉✨💥]+)', text, re.IGNORECASE)",
    "name_match = re.search(r'(?:dự án|project|khu căn hộ|tổ hợp)[ \\t]*[:\\-–]?[ \\t]*([^\\n\\r,;🔥🌟👉✨💥]+)', text, re.IGNORECASE)"
)
# Also fix my drive title patch to strip [ ] and check if it contains drive.google.com
content = content.replace(
    'if (not project_name or project_name.startswith("http") or "drive.google.com" in project_name) and (links["drive"] or links["sheets"]):',
    'if (not project_name or project_name.startswith("http") or "drive.google.com" in project_name or "docs.google.com" in project_name) and (links["drive"] or links["sheets"]):'
)

with open('workflow_api.py', 'w') as f:
    f.write(content)
