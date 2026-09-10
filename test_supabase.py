from database import load_projects_from_database, ensure_database
import traceback
try:
    ensure_database()
    projects = load_projects_from_database()
    print("Found projects:", len(projects))
    if len(projects) == 0:
        print("Wait, projects list is EMPTY!")
except Exception as e:
    print("ERROR OCCURRED:")
    traceback.print_exc()
