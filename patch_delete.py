with open('database.py', 'r') as f:
    content = f.read()

old_del_db = """def delete_project_from_db(project_id: str) -> bool:
    with connect() as connection:
        res = connection.execute("DELETE FROM Projects WHERE id=?", (project_id,))"""
new_del_db = """def delete_project_from_db(project_id: str, required_broker_id: str = None) -> bool:
    with connect() as connection:
        if required_broker_id:
            res = connection.execute("DELETE FROM Projects WHERE id=? AND broker_id=?", (project_id, required_broker_id))
        else:
            res = connection.execute("DELETE FROM Projects WHERE id=?", (project_id,))"""

content = content.replace(old_del_db, new_del_db)
with open('database.py', 'w') as f:
    f.write(content)


with open('workflow_api.py', 'r') as f:
    content = f.read()

old_del_wf = """def delete_project(project_id: str) -> dict[str, Any]:
    deleted = delete_project_from_db(project_id)"""
new_del_wf = """def delete_project(project_id: str, role: str = "admin", broker_id: str = "") -> dict[str, Any]:
    req_broker = broker_id if role == "broker" else None
    deleted = delete_project_from_db(project_id, req_broker)"""

content = content.replace(old_del_wf, new_del_wf)
with open('workflow_api.py', 'w') as f:
    f.write(content)


with open('frontend_server.py', 'r') as f:
    content = f.read()

old_del_route = """            elif endpoint == "/api/projects/delete":
                if not self._require_auth(allowed_roles=["admin"]): return
                pid = str(payload.get("project_id", ""))
                self._send_json(delete_project(pid))"""
new_del_route = """            elif endpoint == "/api/projects/delete":
                session = self._require_auth(allowed_roles=["admin", "broker"])
                if not session: return
                pid = str(payload.get("project_id", ""))
                self._send_json(delete_project(pid, role=session["role"], broker_id=session.get("user_id", "")))"""

content = content.replace(old_del_route, new_del_route)
with open('frontend_server.py', 'w') as f:
    f.write(content)
