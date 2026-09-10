from workflow_api import list_projects
projects = list_projects()
print("Found projects:", len(projects))
