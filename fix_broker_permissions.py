with open('frontend_server.py', 'r') as f:
    content = f.read()

content = content.replace(
    'elif endpoint == "/api/projects/parse-text":\n                if not self._require_auth(allowed_roles=["admin"]): return',
    'elif endpoint == "/api/projects/parse-text":\n                if not self._require_auth(allowed_roles=["admin", "broker"]): return'
)
content = content.replace(
    'elif endpoint == "/api/projects":\n                if not self._require_auth(allowed_roles=["admin"]): return\n                self._send_json(create_or_update_project(payload))',
    'elif endpoint == "/api/projects":\n                if not self._require_auth(allowed_roles=["admin", "broker"]): return\n                self._send_json(create_or_update_project(payload))'
)

with open('frontend_server.py', 'w') as f:
    f.write(content)
