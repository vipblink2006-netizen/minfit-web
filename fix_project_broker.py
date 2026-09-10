with open('frontend_server.py', 'r') as f:
    content = f.read()

content = content.replace(
    'elif endpoint == "/api/projects":\n                if not self._require_auth(allowed_roles=["admin", "broker"]): return\n                self._send_json(create_or_update_project(payload))',
    'elif endpoint == "/api/projects":\n                session = self._require_auth(allowed_roles=["admin", "broker"])\n                if not session: return\n                if session["role"] == "broker":\n                    payload["broker_id"] = session["user_id"]\n                self._send_json(create_or_update_project(payload))'
)

with open('frontend_server.py', 'w') as f:
    f.write(content)
