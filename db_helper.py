
class DBHelper:
    @staticmethod
    def initialize_persistence(database_name):
        import sqlite3
        conn = sqlite3.connect(database_name)
        table_list = DBHelper.get_table_query_list()
        
    
    @staticmethod
    def get_table_query_list():
        create_table_queries = [
            '''CREATE TABLE IF NOT EXISTS Level (
                ID INTEGER PRIMARY KEY,
                LevelName TEXT
            )''',
            '''CREATE TABLE IF NOT EXISTS Platform (
                ID INTEGER PRIMARY KEY,
                x INTEGER,
                y INTEGER,
                width INTEGER,
                height INTEGER,
                type INTEGER,
                LevelName INTEGER,
                FOREIGN KEY (LevelName) REFERENCES Level(ID)
            )'''
        ]
        return create_table_queries