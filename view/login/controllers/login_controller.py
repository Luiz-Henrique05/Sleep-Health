import sqlite3

class LoginController:
    def __init__(self, login_callback):
        self.login_callback = login_callback

    def login(self, username, password, cursor: sqlite3.Cursor):
        try:
            cursor.execute("SELECT * FROM usuarios WHERE username = ? AND senha = ?", (username, password))
            return cursor.fetchone()
        except sqlite3.IntegrityError:
            return "Usuário ou senha inválidos."
        