import customtkinter as ctk
from tkinter import messagebox
    
def tela_cadastro(self, register):
        self.limpar_tela()
        frame = ctk.CTkFrame(self.root, corner_radius=20)
        frame.pack(expand=True, padx=40, pady=50)

        ctk.CTkLabel(frame, text="Cadastro de Usuário", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=10)
        entry_user = ctk.CTkEntry(frame, width=300, placeholder_text="Usuário")
        entry_user.pack(pady=8)
        entry_pass = ctk.CTkEntry(frame, width=300, placeholder_text="Senha", show="*")
        entry_pass.pack(pady=8)

        def cadastrar():
            resultado = register(entry_user.get(), entry_pass.get())
            if resultado is True:
                messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso.")
                self.tela_login()
            else:
                messagebox.showerror("Erro", resultado) 


        ctk.CTkButton(frame, text="Cadastrar", command=cadastrar, width=200).pack(pady=15)
        ctk.CTkButton(frame, text="Voltar", command=self.tela_login, width=200).pack()