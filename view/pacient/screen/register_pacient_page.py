import customtkinter as ctk

from view.pacient.controller.fields import *
from services.database.db import Database
from services.database.queries import *
from view.pacient.screen.components import fields_component

def page(self):
    popup = ctk.CTkToplevel(self.root)
    popup.title("Cadastro de Paciente")
    popup.geometry("480x600")

    frame = ctk.CTkFrame(popup)
    frame.pack(padx=15, pady=15, fill="both", expand=True)
    popup.lift()
    popup.attributes('-topmost', True)
    popup.after(10, lambda: popup.attributes('-topmost', False))

    ctk.CTkLabel(frame, text="Cadastro de Paciente", font=ctk.CTkFont(size=22, weight="bold")).grid(
        row=0, column=0, columnspan=2, pady=10
    )

    entries, linha_final = fields_component.criar_campos_input(frame)

    label_status = ctk.CTkLabel(frame, text="")
    label_status.grid(row=linha_final, column=0, columnspan=2, sticky="w", pady=(10, 0))

    def save():
        try:
            data = {
                "nome": entries[Field.NOME].get(),
                "idade": int(entries[Field.IDADE].get()),
                "genero": entries[Field.GENERO].get(),
                "ocupacao": entries[Field.OCUPACAO].get(),
                "duracao_sono": float(entries[Field.DURACAO_SONO].get()),
                "qualidade_sono": QUALIDADE_SONO_MAP[entries[Field.QUALIDADE_SONO].get()],
                "atividade_fisica": ATIVIDADE_FISICA_MAP[entries[Field.ATIVIDADE_FISICA].get()],
                "passos_diarios": int(entries[Field.PASSOS_DIARIOS].get()),
                "categoria_bmi": CATEGORIA_BMI_MAP[entries[Field.CATEGORIA_BMI].get()],
                "nivel_estresse": STRESS_MAP[entries[Field.NIVEL_ESTRESSE].get()],
                "frequencia_cardiaca": int(entries[Field.FREQUENCIA_CARDIACA].get()),
                "dist_sono": int(entries[Field.DIST_SONO].get())
            }

            db = Database("sono.db")
            db.execute(INSERIR_PACIENTE, tuple(data.values()))
            label_status.configure(text="Paciente cadastrado com sucesso!", text_color="green")
            popup.after(2000, popup.destroy) 
        except Exception as e:
            label_status.configure(text=f"Erro: {e}", text_color="red")

    ctk.CTkButton(frame, text="Salvar", command=save, width=200).grid(
        row=linha_final + 1, column=0, columnspan=2, pady=10
    )


