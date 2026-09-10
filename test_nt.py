from collections import namedtuple
Row = namedtuple('Row', ['project_id'])
r = Row('p1')
try:
    print(r["project_id"])
except Exception as e:
    print("Error:", repr(e))
