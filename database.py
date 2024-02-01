import json

class Database:
    def __init__(self, db_path='info.json'):
        self.db_path = db_path
        
    def _load_data(self):
        try:
            with open(self.db_path) as f:
                return json.load(f)
        except Exception as e:
            print(f"Error Loading data from {self.db_path}: {e}...")
            return None
        
    def _save_data(self, data):
        try:
            with open(self.db_path) as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving data to {self.db_path}: {e}...")
            
    def get_prefix(self, guild_id):
        data = self._load_data()
        return data.get(str(guild_id), '!')
    
    def set_prefix(self, guild_id, prefix):
        data = self._load_data()
        data[str(guild_id)] = prefix
        self._save_data(data)
        
    def remove_prefix(self, guild_id):
        data = self._load_data()
        data.pop(str(guild_id), None)
        self._save_data(data)
        