import json
from workflow_api import list_projects
from frontend_server import CustomJSONEncoder
import traceback

try:
    projects = list_projects(broker_id="brk_moigioi")
    print("Found projects:", len(projects))
    payload = {"projects": projects}
    body = json.dumps(payload, cls=CustomJSONEncoder, ensure_ascii=False).encode("utf-8")
    print("JSON dumped successfully, length:", len(body))
except Exception as e:
    print("ERROR OCCURRED:")
    traceback.print_exc()
