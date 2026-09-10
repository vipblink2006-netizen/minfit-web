from workflow_api import list_projects
import traceback
try:
    projects = list_projects(broker_id="brk_moigioi")
    print("Found projects:", len(projects))
except Exception as e:
    print("ERROR OCCURRED:")
    traceback.print_exc()
