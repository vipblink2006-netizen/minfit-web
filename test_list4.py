from workflow_api import list_projects
projects = list_projects(broker_id="brk_moigioi")
print("Found projects for moigioi:", len(projects))
for p in projects:
    if p["created_by_role"] == "broker":
        print(f"- Broker Project: {p['name']} (ID: {p['id']}, Broker: {p.get('broker_id')})")
