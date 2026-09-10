from database import PostgresCursorWrapper
class DummyCursor:
    def __init__(self):
        self.rowcount = 0
    def execute(self, q, p=None):
        print("EXECUTING:", q)
        return self
wrapper = PostgresCursorWrapper(DummyCursor())
wrapper.execute("INSERT OR REPLACE INTO ProjectAmenities(project_id, amenity_code) VALUES (?,?)", ("a", "b"))
