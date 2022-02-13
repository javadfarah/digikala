import pymongo

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Database(metaclass=Singleton):
    
    def __init__(self, uri):
        self.client = pymongo.MongoClient(uri)

    def search_query(self, query: dict, db_name: str, col_name: str):
        my_db = self.client[db_name]
        my_col = my_db[col_name]
        result = my_col.find_one(query)
        return result

    def insert_query(self, query: dict, db_name: str, col_name: str):
        my_db = self.client[db_name]
        my_col = my_db[col_name]
        result = my_col.insert_one(query)
        return result




