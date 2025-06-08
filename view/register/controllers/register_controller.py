import sqlite3

class RegisterController:
    def __init__(self, register_callback):
        self.register_callback = register_callback

    def register(self, username, password, connection, cursor):
        erro = self.validateRegister(username, password, cursor)
        if erro:
            return erro
        try:
            cursor.execute("INSERT INTO usuarios (username, senha) VALUES (?, ?)", (username, password))
            connection.commit()
            return True
        except sqlite3.IntegrityError:
            return "Erro interno: não foi possível cadastrar usuário."

    def validateRegister(self, username, password, cursor):
        if not username or not password:
            return "Nome de usuário e senha são obrigatórios."
        if len(username) < 3 or len(password) < 6:
            return "Nome de usuário e senha devem ter no mínimo 3 e 6 caracteres."
        cursor.execute("SELECT * FROM usuarios WHERE username = ?", (username,))
        if cursor.fetchone():
            return "Usuário já cadastrado."
        return None
