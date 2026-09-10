with open('frontend_server.py', 'r') as f:
    content = f.read()

content = content.replace(
    'except (ValueError, TypeError, json.JSONDecodeError) as error:\n            self._api_error(error)',
    'except Exception as error:\n            import traceback\n            traceback.print_exc()\n            self._api_error(error, 500)'
)

with open('frontend_server.py', 'w') as f:
    f.write(content)
