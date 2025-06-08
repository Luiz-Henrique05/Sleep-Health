import customtkinter as ctk    
    
def home_screen(self):
        self.limpar_tela()
        frame = ctk.CTkFrame(self.root)
        frame.pack(expand=True, padx=40, pady=30)
        ctk.CTkLabel(frame, text=f"Bem-vindo, {self.usuario_logado}!", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=20)

        buttons = [
            ("Cadastrar Paciente", self.tela_cadastro_paciente),
            ("Consultar Pacientes", self.tela_consulta_pacientes),
            ("Importar Pacientes CSV", self.importar_pacientes_csv),
            ("Consultas Avançadas", self.tela_consultas_avancadas),
            ("Estatísticas Gerais", self.tela_estatisticas),
            ("Médias por Categoria", self.tela_medias),
            ("Simulador de Sono", self.tela_simulador),
            ("Exportar CSV", self.exportar_csv),
            ("Backup do Banco", self.fazer_backup),
            ("Sair", self.root.destroy),
        ]

        grid = ctk.CTkFrame(frame)
        grid.pack()
        for i, (texto, comando) in enumerate(buttons):
            btn = ctk.CTkButton(grid, text=texto, command=comando, width=240)
            btn.grid(row=i // 2, column=i % 2, padx=15, pady=10)