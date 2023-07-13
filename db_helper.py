import sqlite3
from constantes import *
class DBHelper:

    @staticmethod
    def initialize_persistence(database_name = DATABASE_NAME):
        with sqlite3.connect(f"db/{database_name}") as conexion:
            try:
                query = DBHelper.get_score_table_query()
                conexion.execute(query)
                print("Se creo la tabla score")    
            except:
                print("Error initializing persistence")

    @staticmethod
    def get_score_table_query():
        return '''
                create table score (
                id integer primary key autoincrement,
                player_name text,
                score real
                )
                '''.strip()
                
    @staticmethod
    def get_scores(database_name = DATABASE_NAME):
        score_list = []
        scores = []
        with sqlite3.connect(f"db/{database_name}") as conexion:
            try:
                query = DBHelper.get_all_scores_query()
                scores = conexion.execute(query)
            except:
                print("Hubo un error al conectar con base de datos")
        for score in scores:
            score_list.append(score)
        return score_list
        
    @staticmethod
    def get_all_scores_query():
        return '''
            SELECT * FROM score ORDER BY score DESC
            '''.strip()
    @staticmethod
    def get_score_by_name_query(name):
        return f'''
            SELECT * FROM score where player_name = '{name}'
            '''.strip()
    
    @staticmethod
    def set_score_for_player(player, database_name = DATABASE_NAME):
        name = player.get_name()
        score = player.get_score()
        DBHelper.set_score(name, score, database_name)

    @staticmethod
    def set_score(name, score, database_name = DATABASE_NAME):
        with sqlite3.connect(f"db/{database_name}") as conexion:
            query_get = DBHelper.get_score_by_name_query(name)
            rows = conexion.execute(query_get)
            if rows.arraysize <= 1:
                query_set = DBHelper.get_query_set_score(name, score)
            else:
                query_set = DBHelper.get_update_score_query(name, score)
            conexion.execute(query_set)
            conexion.commit()

    @staticmethod
    def get_query_set_score(name, score):
        return f'''
                INSERT INTO score (player_name,score) values ('{name}',{score})
                '''.strip()
    @staticmethod
    def get_update_score_query(name, score):
        return f'''
                UPDATE score SET score = {score} where player_name = '{name}'
                '''.strip()
        
    
    