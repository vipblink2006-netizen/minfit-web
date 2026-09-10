with open('frontend_server.py', 'r') as f:
    content = f.read()

content = content.replace(
    'json.dumps(payload, ensure_ascii=False)',
    'json.dumps(payload, cls=CustomJSONEncoder, ensure_ascii=False)'
)

with open('frontend_server.py', 'w') as f:
    f.write(content)
