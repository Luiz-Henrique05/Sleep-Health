import customtkinter as ctk
from view.pacient.controller.fields import (
    Field, FIELD_TYPES,
    QUALIDADE_SONO_MAP, ATIVIDADE_FISICA_MAP, CATEGORIA_BMI_MAP, STRESS_MAP
)
from view.pacient.controller.edit_pacient_controller import EditPacientController

def criar_campos_input(parent, dados=None):
    entries = {}
    ocupacoes = EditPacientController().get_ocupations()
    reverse_maps = {
        Field.QUALIDADE_SONO: {v: k for k, v in QUALIDADE_SONO_MAP.items()},
        Field.ATIVIDADE_FISICA: {v: k for k, v in ATIVIDADE_FISICA_MAP.items()},
        Field.NIVEL_ESTRESSE: {v: k for k, v in STRESS_MAP.items()},
    }

    linha = 1

    for field in Field:
        ctk.CTkLabel(parent, text=field.value + ":").grid(row=linha, column=0, sticky="w", padx=10, pady=4)

        if field == Field.OCUPACAO:
            entry = ctk.CTkEntry(parent, width=220)
            entry.grid(row=linha, column=1, padx=10, pady=4)
            entries[field] = entry

            suggestion_frame = ctk.CTkFrame(parent)
            suggestion_frame.grid(row=linha + 1, column=1, padx=10, sticky="w")
            suggestion_frame.grid_remove()

            def atualizar(event, e=entry, frame=suggestion_frame):
                for w in frame.winfo_children():
                    w.destroy()
                texto = e.get().lower()
                if not texto:
                    frame.grid_remove()
                    return
                sugestoes = [o for o in ocupacoes if texto in o.lower()]
                if not sugestoes:
                    frame.grid_remove()
                    return
                frame.grid()
                for item in sugestoes[:5]:
                    btn = ctk.CTkButton(frame, text=item, width=220, height=20,
                        command=lambda val=item: (e.delete(0, "end"), e.insert(0, val), frame.grid_remove()))
                    btn.pack(anchor="w", pady=1)

            entry.bind("<KeyRelease>", atualizar)

            if dados:
                entry.insert(0, str(dados[list(Field).index(field) + 1]))

            linha += 2
        else:
            tipo = FIELD_TYPES.get(field, {"type": "entry"})
            if tipo["type"] == "combo":
                entry = ctk.CTkComboBox(parent, values=tipo["values"], width=220, state="readonly")
                if dados:
                    valor = dados[list(Field).index(field) + 1]
                    if field in reverse_maps:
                        valor = reverse_maps[field].get(valor, valor)
                    entry.set(str(valor))
            else:
                entry = ctk.CTkEntry(parent, width=220)
                if dados:
                    entry.insert(0, str(dados[list(Field).index(field) + 1]))
            entry.grid(row=linha, column=1, padx=10, pady=4)
            entries[field] = entry
            linha += 1

    return entries, linha
