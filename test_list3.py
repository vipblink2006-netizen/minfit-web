from workflow_api import list_projects
import json
from frontend_server import CustomJSONEncoder

projects = list_projects(broker_id="brk_moigioi")
print("Found projects:", len(projects))
payload = {"projects": projects}
body = json.dumps(payload, cls=CustomJSONEncoder, ensure_ascii=False)
print("Length of JSON payload:", len(body))
print("First project:", body[:500])
