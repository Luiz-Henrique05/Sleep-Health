import customtkinter as ctk
    
def login_screen(self, clear):
    clear()
    frame = ctk.CTkFrame(self.root, corner_radius=20)
    frame.pack(expand=True, padx=40, pady=45)

    ctk.CTkLabel(frame, text="Login", font=ctk.CTkFont(size=26, weight="bold")).pack(pady=(10, 20))

    ctk.CTkLabel(frame, text="Usuário:").pack(anchor="w", padx=10)
    self.entry_user = ctk.CTkEntry(frame, width=300, placeholder_text="Digite seu usuário...", justify="left")
    self.entry_user.pack(padx=10, pady=(0, 15))

    ctk.CTkLabel(frame, text="Senha:").pack(anchor="w", padx=10)
    self.entry_pass = ctk.CTkEntry(frame, width=300, show="*", placeholder_text="Digite sua senha...", justify="left")
    self.entry_pass.pack(padx=10, pady=(0, 5))

    self.login_msg = ctk.CTkLabel(frame, text="", text_color="red")
    if self.usuario_logado:
        self.login_msg.pack(pady=(0, 10))
            
    ctk.CTkButton(frame, text="Entrar", command=self.tentar_login, width=200).pack(pady=(15, 10))
    ctk.CTkButton(frame, text="Cadastrar Novo Usuário", command=self.register_page, width=200).pack(pady=(5, 5))
