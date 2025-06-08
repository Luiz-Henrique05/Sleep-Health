import sqlite3

class Database:
    def __init__(self, db_name: str):
        self.db = None
        self.cursor = None
        self._connect(db_name)

    def _connect(self, db_name: str):
        try:
            self.db = sqlite3.connect(db_name)
            self.cursor = self.db.cursor()
            print(f"Conexão estabelecida com o banco de dados {db_name}.")
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")

    def create(self, query: str):
        try:
            self.cursor.execute(query)
            self.db.commit()
            print("Tabela criada com sucesso.")
        except sqlite3.Error as e:
            print(f"Erro ao criar tabela: {e}")

    def execute(self, query: str, params: tuple = ()):
        try:
            self.cursor.execute(query, params)
            self.db.commit()
            print("Query executada com sucesso.")
            self.close()
        except sqlite3.Error as e:
            print(f"Erro ao executar query: {e}")

    def fetchall(self, query: str, params: tuple = ()):
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erro ao buscar dados: {e}")
            return None
        
    def fetchone(self, query: str, params: tuple = ()):
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Erro ao buscar um único dado: {e}")
            return None

    def close(self):
        if self.db:
            self.db.close()
            print("Conexão encerrada.")
