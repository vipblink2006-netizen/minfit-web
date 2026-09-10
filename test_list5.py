from database import load_projects_from_database
projects = load_projects_from_database(broker_id="brk_moigioi")
found = False
for p in projects:
    if p.id == 'prj_0_1700':
        print("FOUND IN LOAD_PROJECTS_FROM_DATABASE!")
        found = True
if not found:
    print("NOT FOUND IN LOAD_PROJECTS_FROM_DATABASE!")
