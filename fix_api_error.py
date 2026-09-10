with open('frontend_server.py', 'r') as f:
    content = f.read()

content = content.replace(
    'self._api_error(error, 500)',
    'self._api_error(error)'
)

with open('frontend_server.py', 'w') as f:
    f.write(content)
