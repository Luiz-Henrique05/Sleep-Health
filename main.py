import customtkinter as ctk

from services.database.queries import *
from view.gui import App
from view.console.console_test import ConsoleTest
    
if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")

    consoleMode = False  # Mude para true para usar o console
    root = ctk.CTk()
    app = App(root)
    
    if consoleMode:
        ConsoleTest().menu()
        root.mainloop()
    else:
        app
        root.mainloop()
    