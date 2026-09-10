with open('workflow_api.py', 'r') as f:
    content = f.read()

content = content.replace("last_active = 'Vừa xong'", "last_active = CURRENT_TIMESTAMP")

with open('workflow_api.py', 'w') as f:
    f.write(content)
