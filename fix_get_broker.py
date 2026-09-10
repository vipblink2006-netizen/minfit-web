import re
with open('frontend_server.py', 'r') as f:
    content = f.read()

replacement = """        if endpoint == "/api/projects":
            try:
                broker_id = query.get("broker_id", [None])[0]
                if broker_id == 'broker_default':
                    session = self._get_authenticated_session()
                    if session and session['role'] == 'broker':
                        broker_id = session['user_id']
                    else:
                        broker_id = None
"""
content = re.sub(r'        if endpoint == "/api/projects":\n            try:\n                broker_id = query.get\("broker_id", \[None\]\)\[0\]\n', replacement, content)

with open('frontend_server.py', 'w') as f:
    f.write(content)
