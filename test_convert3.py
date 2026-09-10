from database import PostgresCursorWrapper
class DummyCursor:
    def __init__(self):
        self.rowcount = 0
    def execute(self, q, p=None):
        print("EXECUTING:", q)
        return self
wrapper = PostgresCursorWrapper(DummyCursor())
wrapper.execute("SELECT * FROM Projects WHERE is_global = 1 OR broker_id = ?", ("brk_moigioi",))
