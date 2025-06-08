import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk
import sqlite3, pandas as pd, matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from view.components.back_screen_button import back_screen_button
from view.register.screen import register_page
from view.login.screen import login_page
from view.home.screen import home_page
from view.pacient.screen import register_pacient_page
from view.pacient.screen import edit_pacient_page

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.app_services import (
    import_csv, simular_sono, exportar_para_csv, backup_banco, register, login
)

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Saúde do Sono")
        self.root.geometry("900x620")
        self.usuario_logado = None
        self.tela_login()

    def limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def tela_login(self):
        login_page.login_screen(self, self.limpar_tela)

    def tentar_login(self):
        usuario = self.entry_user.get()
        senha = self.entry_pass.get()
        if login(usuario, senha):
            self.usuario_logado = usuario
            self.tela_boas_vindas()
        else:
            self.login_msg.configure(text="Usuário ou senha inválidos.")

    def register_page(self):
        register_page.tela_cadastro(self, register=register)

    def tela_boas_vindas(self):
        home_page.home_screen(self)

    def tela_cadastro_paciente(self):
        register_pacient_page.page(self)

    def tela_consulta_pacientes(self):
        edit_pacient_page.page(self)
        
    def importar_pacientes_csv(self):
        caminho = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if caminho:
            try:
                import_csv(caminho)
                messagebox.showinfo("Importação", "Pacientes importados com sucesso.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao importar CSV: {e}")

    def tela_consultas_avancadas(self):
        messagebox.showinfo("A implementar", "ainda a ser feito.")

# Tela de Estatísticas com gráficos e dados

    def tela_estatisticas(self):
        self.limpar_tela()

        frame = ctk.CTkFrame(self.root, fg_color="transparent")
        frame.pack(padx=30, pady=30, fill="both", expand=True)

        # Carregar dados do banco
        conn = sqlite3.connect("sono.db")
        df = pd.read_sql_query("SELECT * FROM pacientes", conn)
        conn.close()

        # Bloco estatísticas básicas com cantos arredondados e fundo suave
        bloco_estatisticas = ctk.CTkFrame(frame, fg_color="#f5f5f5", corner_radius=15)
        bloco_estatisticas.pack(pady=10, padx=20, fill="x")

        media_idade = df['idade'].mean() if not df.empty else 0
        media_qualidade = df['qualidade_sono'].mean() if not df.empty else 0

        ctk.CTkLabel(
            bloco_estatisticas,
            text=f"Média de Idade: {media_idade:.2f}",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=6)
        ctk.CTkLabel(
            bloco_estatisticas,
            text=f"Média da Qualidade do Sono: {media_qualidade:.2f}",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=6)

        ctk.CTkButton(bloco_estatisticas, text="Voltar", command=self.tela_boas_vindas, width=150,
                      corner_radius=15).pack(pady=15)

        # Frame para os gráficos, com layout grid centralizado
        graficos_frame = ctk.CTkFrame(frame, fg_color="transparent")
        graficos_frame.pack(fill="both", expand=True, pady=5)

        # Ajustar tamanho e estilo dos gráficos
        figsize = (5, 4)  # maior para mais vertical

        # Gráfico 1: Distribuição das Idades
        fig1, ax1 = plt.subplots(figsize=figsize)
        df['idade'].plot(kind='hist', bins=15, ax=ax1, color='skyblue', edgecolor='black')
        ax1.set_title("Distribuição das Idades", fontsize=14, weight='bold')
        ax1.set_xlabel("Idade")
        ax1.set_ylabel("Quantidade")
        ax1.grid(True, linestyle='--', alpha=0.5)

        canvas1 = FigureCanvasTkAgg(fig1, master=graficos_frame)
        canvas1.draw()
        canvas1.get_tk_widget().grid(row=0, column=0, padx=15, pady=10, sticky="nsew")

        # Gráfico 2: Média da Qualidade do Sono por Gênero
        fig2, ax2 = plt.subplots(figsize=figsize)
        df.groupby("genero")["qualidade_sono"].mean().plot(kind="bar", color='mediumpurple', ax=ax2, edgecolor='black')
        ax2.set_title("Média da Qualidade do Sono por Gênero", fontsize=12, weight='bold')
        ax2.set_ylabel("Qualidade Média")
        ax2.set_xlabel("Gênero")
        ax2.grid(axis='y', linestyle='--', alpha=0.5)

        canvas2 = FigureCanvasTkAgg(fig2, master=graficos_frame)
        canvas2.draw()
        canvas2.get_tk_widget().grid(row=0, column=1, padx=15, pady=10, sticky="nsew")

        # Gráfico 3: Frequência de Distúrbios (coluna 'dist_sono')
        fig3, ax3 = plt.subplots(figsize=figsize)
        if 'dist_sono' in df.columns and not df['dist_sono'].isna().all():
            df['dist_sono'].value_counts().plot(kind='bar', color='salmon', ax=ax3, edgecolor='black')
            ax3.set_title("Frequência de Distúrbios do Sono", fontsize=12, weight='bold')
            ax3.set_ylabel("Quantidade")
            ax3.set_xlabel("Distúrbio")
            ax3.grid(axis='y', linestyle='--', alpha=0.5)
        else:
            ax3.text(0.5, 0.5, "Sem dados disponíveis", ha='center', va='center', fontsize=12, color='gray')
            ax3.axis('off')

        canvas3 = FigureCanvasTkAgg(fig3, master=graficos_frame)
        canvas3.draw()
        canvas3.get_tk_widget().grid(row=0, column=2, padx=15, pady=10, sticky="nsew")

        # Gráfico 4: Atividade Física vs Qualidade do Sono
        fig4, ax4 = plt.subplots(figsize=figsize)
        if 'atividade_fisica' in df.columns and 'qualidade_sono' in df.columns:
            ax4.scatter(df['atividade_fisica'], df['qualidade_sono'], color='green', alpha=0.6, edgecolor='black')
            ax4.set_title("Atividade Física vs Qualidade do Sono", fontsize=12, weight='bold')
            ax4.set_xlabel("Atividade Física")
            ax4.set_ylabel("Qualidade do Sono")
            ax4.grid(True, linestyle='--', alpha=0.5)
        else:
            ax4.text(0.5, 0.5, "Sem dados disponíveis", ha='center', va='center', fontsize=12, color='gray')
            ax4.axis('off')

        canvas4 = FigureCanvasTkAgg(fig4, master=graficos_frame)
        canvas4.draw()
        canvas4.get_tk_widget().grid(row=0, column=3, padx=15, pady=10, sticky="nsew")

        # Configurar grid para expansão igualitária dos gráficos
        for col in range(4):
            graficos_frame.grid_columnconfigure(col, weight=1)
        graficos_frame.grid_rowconfigure(0, weight=1)

    def tela_medias(self):
        self.limpar_tela()
        frame = ctk.CTkFrame(self.root)
        frame.pack(padx=30, pady=30, fill="both", expand=True)

        conn = sqlite3.connect("sono.db")
        df = pd.read_sql_query("SELECT categoria_bmi, qualidade_sono FROM pacientes", conn)
        conn.close()

        medias = df.groupby('categoria_bmi')['qualidade_sono'].mean()

        linha_topo = ctk.CTkFrame(frame)
        linha_topo.pack(fill="x", pady=10, padx=10)

        back_screen_button(linha_topo, self.tela_boas_vindas).grid(row=0, column=0, padx=(0, 10))
        ctk.CTkLabel(
            linha_topo,
            text="Média da Qualidade do Sono por Categoria de IMC",
            font=ctk.CTkFont(size=14)
        ).grid(row=0, column=1, sticky="w")

        grafico_frame = ctk.CTkFrame(frame)
        grafico_frame.pack(fill="both", expand=True)

        fig, ax = plt.subplots(figsize=(6, 4))
        medias.plot(kind='bar', ax=ax, color='lightgreen')
        ax.set_title("Qualidade do Sono por Categoria de IMC")
        ax.set_xlabel("Categoria de IMC")
        ax.set_ylabel("Qualidade do Sono")

        canvas = FigureCanvasTkAgg(fig, master=grafico_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=10)

    def tela_simulador(self):
        simular_sono()

    def exportar_csv(self):
        exportar_para_csv()

    def fazer_backup(self):
        backup_banco()