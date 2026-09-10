import workflow_api
try:
    workflow_api._ensure_workflow_tables()
except Exception as e:
    import traceback
    traceback.print_exc()
