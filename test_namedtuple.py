from collections import namedtuple
Row = namedtuple('Row', ['id', 'name'])
r = Row('usr_admin', 'Chinh chu')
try:
    print(dict(r))
except Exception as e:
    print("Error:", repr(e))
