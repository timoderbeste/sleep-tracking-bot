class DatabaseHandler:
    def __init__(self):
        pass
    
    def save_data(self, key, value):
        raise NotImplementedError
    
    def load_data(self, key):
        raise NotImplementedError
    
    
class MockDatabaseHandler(DatabaseHandler):
    def __init__(self):
        super().__init__()
        self.database = dict()
    
    def save_data(self, key, value):
        self.database[key] = value

    def load_data(self, key):
        return self.database[key] if key in self.database else None


mock_database_handler = MockDatabaseHandler()
