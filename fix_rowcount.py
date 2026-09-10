with open('database.py', 'r') as f:
    content = f.read()

content = content.replace(
    '    def fetchval(self): \n        row = self._cursor.fetchone()\n        return row[0] if row else None',
    '    def fetchval(self): \n        row = self._cursor.fetchone()\n        return row[0] if row else None\n    @property\n    def rowcount(self):\n        return self._cursor.rowcount'
)

with open('database.py', 'w') as f:
    f.write(content)
