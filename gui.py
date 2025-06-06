import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk
import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from main import (
    validar_login, cadastrar_usuario, importar_csv,
    simular_sono, exportar_para_csv, backup_banco
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
        self.limpar_tela()
        frame = ctk.CTkFrame(self.root, corner_radius=20)
        frame.pack(expand=True, padx=40, pady=45)

        ctk.CTkLabel(frame, text="Login", font=ctk.CTkFont(size=26, weight="bold")).pack(pady=10)
        ctk.CTkLabel(frame, text="Usuário:").pack(anchor="w", padx=10)
        self.entry_user = ctk.CTkEntry(frame, width=300)
        self.entry_user.pack(pady=5)
        ctk.CTkLabel(frame, text="Senha:").pack(anchor="w", padx=10)
        self.entry_pass = ctk.CTkEntry(frame, width=300, show="*")
        self.entry_pass.pack(pady=5)
        self.login_msg = ctk.CTkLabel(frame, text="", text_color="red")
        self.login_msg.pack()

        ctk.CTkButton(frame, text="Entrar", command=self.tentar_login, width=200).pack(pady=15)
        ctk.CTkButton(frame, text="Cadastrar Novo Usuário", command=self.tela_cadastro, width=200).pack()

    def tentar_login(self):
        usuario = self.entry_user.get()
        senha = self.entry_pass.get()
        if validar_login(usuario, senha):
            self.usuario_logado = usuario
            self.tela_boas_vindas()
        else:
            self.login_msg.configure(text="Usuário ou senha inválidos.")

    def tela_cadastro(self):
        self.limpar_tela()
        frame = ctk.CTkFrame(self.root, corner_radius=20)
        frame.pack(expand=True, padx=40, pady=50)

        ctk.CTkLabel(frame, text="Cadastro de Usuário", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=10)
        entry_user = ctk.CTkEntry(frame, width=300, placeholder_text="Usuário")
        entry_user.pack(pady=8)
        entry_pass = ctk.CTkEntry(frame, width=300, placeholder_text="Senha", show="*")
        entry_pass.pack(pady=8)

        def cadastrar():
            if cadastrar_usuario(entry_user.get(), entry_pass.get()):
                messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso.")
                self.tela_login()
            else:
                messagebox.showerror("Erro", "Usuário já existe.")

        ctk.CTkButton(frame, text="Cadastrar", command=cadastrar, width=200).pack(pady=15)
        ctk.CTkButton(frame, text="Voltar", command=self.tela_login, width=200).pack()

    def tela_boas_vindas(self):
        self.limpar_tela()
        frame = ctk.CTkFrame(self.root)
        frame.pack(expand=True, padx=40, pady=30)
        ctk.CTkLabel(frame, text=f"Bem-vindo, {self.usuario_logado}!", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=20)

        botoes = [
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
        for i, (texto, comando) in enumerate(botoes):
            btn = ctk.CTkButton(grid, text=texto, command=comando, width=240)
            btn.grid(row=i // 2, column=i % 2, padx=15, pady=10)

    def tela_cadastro_paciente(self):
        popup = ctk.CTkToplevel(self.root)
        popup.title("Cadastro de Paciente")
        popup.geometry("480x600")

        frame = ctk.CTkFrame(popup)
        frame.pack(padx=15, pady=15, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Cadastro de Paciente", font=ctk.CTkFont(size=22, weight="bold")).grid(row=0, column=0, columnspan=2, pady=10)

        campos = [
            "Nome", "Idade", "Gênero", "Ocupação", "Duração do Sono (h)",
            "Qualidade do Sono (1-10)", "Atividade Física(1-100)", "Passos Diários",
            "Categoria de IMC", "Nível de Estresse (1-10)", "Frequência Cardíaca", "Distúrbio do Sono"
        ]

        entries = {}
        for i, campo in enumerate(campos):
            ctk.CTkLabel(frame, text=campo + ":").grid(row=i+1, column=0, sticky="w", padx=10, pady=4)
            entry = ctk.CTkEntry(frame, width=220)
            entry.grid(row=i+1, column=1, padx=10, pady=4)
            entries[campo] = entry

        label_status = ctk.CTkLabel(frame, text="")
        label_status.grid(row=len(campos)+1, column=0, columnspan=2, pady=10)

        def salvar():
            try:
                dados = {
                    "nome": entries["Nome"].get(),
                    "idade": int(entries["Idade"].get()),
                    "genero": entries["Gênero"].get(),
                    "ocupacao": entries["Ocupação"].get(),
                    "duracao_sono": float(entries["Duração do Sono (h)"].get()),
                    "qualidade_sono": int(entries["Qualidade do Sono (1-10)"].get()),
                    "atividade_fisica": int(entries["Atividade Física(1-100)"].get()),
                    "passos_diarios": int(entries["Passos Diários"].get()),
                    "categoria_bmi": entries["Categoria de IMC"].get(),
                    "nivel_estresse": int(entries["Nível de Estresse (1-10)"].get()),
                    "frequencia_cardiaca": int(entries["Frequência Cardíaca"].get()),
                    "dist_sono": entries["Distúrbio do Sono"].get()
                }
                conn = sqlite3.connect("sono.db")
                cur = conn.cursor()
                cur.execute("""
                    INSERT INTO pacientes (
                        nome, idade, genero, ocupacao, duracao_sono, qualidade_sono,
                        atividade_fisica, passos_diarios, categoria_bmi, nivel_estresse,
                        frequencia_cardiaca, dist_sono
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, tuple(dados.values()))
                conn.commit()
                conn.close()
                label_status.configure(text="Paciente cadastrado com sucesso!", text_color="green")
                for entry in entries.values():
                    entry.delete(0, ctk.END)
            except Exception as e:
                label_status.configure(text=f"Erro: {e}", text_color="red")

        ctk.CTkButton(frame, text="Salvar", command=salvar, width=200).grid(row=len(campos)+2, column=0, columnspan=2, pady=10)

    def tela_consulta_pacientes(self):
        self.limpar_tela()
        frame = ctk.CTkFrame(self.root)
        frame.pack(padx=30, pady=30, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Pacientes Cadastrados", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=10)

        tree = ttk.Treeview(frame, columns=("ID", "Nome", "Idade", "Gênero", "Distúrbio"), show="headings")
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")
        tree.pack(fill="both", expand=True)

        def carregar_pacientes():
            tree.delete(*tree.get_children())
            conn = sqlite3.connect("sono.db")
            cur = conn.cursor()
            cur.execute("SELECT id, nome, idade, genero, dist_sono FROM pacientes")
            for row in cur.fetchall():
                tree.insert("", "end", values=row)
            conn.close()

        carregar_pacientes()

        def excluir_paciente():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Aviso", "Selecione um paciente para excluir.")
                return
            id_paciente = tree.item(selected[0])['values'][0]
            nome_paciente = tree.item(selected[0])['values'][1]
            confirm = messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir o paciente '{nome_paciente}'?")
            if confirm:
                conn = sqlite3.connect("sono.db")
                cur = conn.cursor()
                cur.execute("DELETE FROM pacientes WHERE id = ?", (id_paciente,))
                conn.commit()
                conn.close()
                carregar_pacientes()
                messagebox.showinfo("Sucesso", f"Paciente '{nome_paciente}' excluído com sucesso.")

        def editar_paciente():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Aviso", "Selecione um paciente para editar.")
                return

            id_paciente = tree.item(selected[0])['values'][0]
            conn = sqlite3.connect("sono.db")
            cur = conn.cursor()
            cur.execute("SELECT * FROM pacientes WHERE id = ?", (id_paciente,))
            dados = cur.fetchone()
            conn.close()

            campos = [
                "nome", "idade", "genero", "ocupacao", "duracao_sono", "qualidade_sono",
                "atividade_fisica", "passos_diarios", "categoria_bmi", "nivel_estresse",
                "frequencia_cardiaca", "dist_sono"
            ]

            popup = ctk.CTkToplevel(self.root)
            popup.title("Editar Paciente")
            popup.geometry("500x600")

            frame_edit = ctk.CTkFrame(popup)
            frame_edit.pack(padx=15, pady=15, fill="both", expand=True)

            entries = {}
            for i, campo in enumerate(campos):
                ctk.CTkLabel(frame_edit, text=campo.replace("_", " ").capitalize() + ":").grid(row=i, column=0, sticky="w", padx=10, pady=4)
                entry = ctk.CTkEntry(frame_edit, width=220)
                entry.insert(0, str(dados[i+1]))  # +1 pois id é o primeiro
                entry.grid(row=i, column=1, padx=10, pady=4)
                entries[campo] = entry

            def salvar_alteracoes():
                try:
                    valores = [entry.get() for entry in entries.values()]
                    valores[1] = int(valores[1])  # idade
                    valores[4] = float(valores[4])  # duracao_sono
                    valores[5] = int(valores[5])  # qualidade
                    valores[6] = int(valores[6])  # atividade
                    valores[7] = int(valores[7])  # passos
                    valores[9] = int(valores[9])  # estresse
                    valores[10] = int(valores[10])  # freq cardíaca

                    conn = sqlite3.connect("sono.db")
                    cur = conn.cursor()
                    cur.execute(f"""
                        UPDATE pacientes SET
                            nome=?, idade=?, genero=?, ocupacao=?, duracao_sono=?,
                            qualidade_sono=?, atividade_fisica=?, passos_diarios=?,
                            categoria_bmi=?, nivel_estresse=?, frequencia_cardiaca=?, dist_sono=?
                        WHERE id = ?
                    """, (*valores, id_paciente))
                    conn.commit()
                    conn.close()
                    carregar_pacientes()
                    popup.destroy()
                    messagebox.showinfo("Sucesso", "Paciente atualizado com sucesso.")
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao salvar alterações: {e}")

            ctk.CTkButton(frame_edit, text="Salvar Alterações", command=salvar_alteracoes).grid(row=len(campos), column=0, columnspan=2, pady=10)

        # Botões
        btn_frame = ctk.CTkFrame(frame)
        btn_frame.pack(pady=10)
        ctk.CTkButton(btn_frame, text="Editar Selecionado", command=editar_paciente, width=180).pack(side="left", pady=5, padx=5)
        ctk.CTkButton(btn_frame, text="Excluir Selecionado", command=excluir_paciente, fg_color="red", hover_color="#8d0b0b",
                       width=180).pack(side="left", pady=5, padx=5)
        ctk.CTkButton(frame, text="Voltar", command=self.tela_boas_vindas, width=200).pack(pady=10)

    def importar_pacientes_csv(self):
        caminho = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if caminho:
            try:
                importar_csv(caminho)
                messagebox.showinfo("Importação", "Pacientes importados com sucesso.")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao importar CSV: {e}")

    def tela_consultas_avancadas(self):
        messagebox.showinfo("A implementar", "ainda a ser feito.")

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
        ax2.set_title("Média da Qualidade do Sono por Gênero", fontsize=14, weight='bold')
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
            ax3.set_title("Frequência de Distúrbios do Sono", fontsize=14, weight='bold')
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
            ax4.set_title("Atividade Física vs Qualidade do Sono", fontsize=14, weight='bold')
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

        ctk.CTkLabel(frame, text="Média da Qualidade do Sono por Categoria de IMC", font=ctk.CTkFont(size=18)).pack(pady=6)

        fig, ax = plt.subplots(figsize=(6,4))
        medias.plot(kind='bar', ax=ax, color='lightgreen')
        ax.set_title("Qualidade do Sono por Categoria de IMC")
        ax.set_xlabel("Categoria de IMC")
        ax.set_ylabel("Qualidade do Sono")

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

        ctk.CTkButton(frame, text="Voltar", command=self.tela_boas_vindas).pack(pady=15)

    def tela_simulador(self):
        simular_sono()

    def exportar_csv(self):
        exportar_para_csv()

    def fazer_backup(self):
        backup_banco()

if __name__ == "__main__":
    root = ctk.CTk()
    app = App(root)
    root.mainloop()
