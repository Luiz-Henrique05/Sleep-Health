import customtkinter as ctk
from tkinter import messagebox, ttk

from view.pacient.controller.edit_pacient_controller import EditPacientController
from view.pacient.controller.fields import *
from view.pacient.screen.components.fields_component import criar_campos_input
from services.database.db import Database
from services.database.queries import BUSCAR_POR_ID

def page(self):
        self.limpar_tela()
        frame = ctk.CTkFrame(self.root)
        frame.pack(padx=30, pady=30, fill="both", expand=True)

        ctk.CTkLabel(frame, text="Pacientes Cadastrados", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=10)

        tree = ttk.Treeview(frame, columns=("ID", "Nome", "Idade", "Gênero", "Distúrbio"), show="headings")
        for col in tree["columns"]:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")
        tree.pack(fill="both", expand=True)
        tree.bind("<Double-1>", lambda event: editar_paciente())

        def getPacients():
            EditPacientController().get(tree)

        def deletePacient():
            EditPacientController().delete(tree)

        def editar_paciente():
            EditPacientController().update(tree)
            db = Database("sono.db")
            id = tree.item(tree.selection())['values'][0]
            data = db.fetchone(BUSCAR_POR_ID, (id,))

            popup = ctk.CTkToplevel(self.root)
            popup.title("Editar Paciente")
            popup.geometry("500x600")

            frame_edit = ctk.CTkFrame(popup)
            frame_edit.pack(padx=15, pady=15, fill="both", expand=True)

            entries, linha_final = criar_campos_input(frame_edit, dados=data)

            def salvar_alteracoes():
                success = EditPacientController().save(entries, id)
                if not success:
                    return
                popup.destroy()
                messagebox.showinfo("Sucesso", "Paciente atualizado com sucesso.")
                getPacients()

            ctk.CTkButton(frame_edit, text="Salvar Alterações", command=salvar_alteracoes).grid(
                row=linha_final, column=0, columnspan=2, pady=10
            )



        btn_frame = ctk.CTkFrame(frame)
        btn_frame.pack(pady=10)
        ctk.CTkButton(btn_frame, text="Editar Selecionado", command=editar_paciente, width=180).pack(side="left", pady=5, padx=5)
        ctk.CTkButton(btn_frame, text="Excluir Selecionado", command=deletePacient, fg_color="red", hover_color="#8d0b0b",
                       width=180).pack(side="left", pady=5, padx=5)
        ctk.CTkButton(frame, text="Voltar", command=self.tela_boas_vindas, width=200).pack(pady=10)
        getPacients()

   