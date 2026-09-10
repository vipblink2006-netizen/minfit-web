with open('frontend_server.py', 'r') as f:
    content = f.read()

# Add a custom json encoder that handles datetime
custom_encoder = """
import datetime
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        return super().default(obj)
"""

if "class CustomJSONEncoder" not in content:
    content = content.replace("import json\n", "import json\n" + custom_encoder)

content = content.replace(
    'json.dumps(data, ensure_ascii=False)',
    'json.dumps(data, cls=CustomJSONEncoder, ensure_ascii=False)'
)

with open('frontend_server.py', 'w') as f:
    f.write(content)
