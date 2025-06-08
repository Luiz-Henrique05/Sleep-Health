from tkinter import messagebox, ttk

from services.database.db import Database
from services.database.queries import *
from view.pacient.controller.fields import  *

class EditPacientController:
    def get(self, tree: ttk.Treeview):
        tree.delete(*tree.get_children())
        
        db = Database("sono.db")
        rows = db.fetchall(SELECIONAR_PACIENTE_EDIT)
        
        for row in rows:
            tree.insert("", "end", values=row)
        db.close()        
        
    def delete(self, tree: ttk.Treeview):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um paciente para excluir.")
            return
        
        id = tree.item(selected[0])['values'][0]
        name = tree.item(selected[0])['values'][1]
        confirm = messagebox.askyesno("Confirmar Exclusão", f"Tem certeza que deseja excluir o paciente '{name}'?")
        if confirm:
            try:
                db = Database("sono.db")
                db.execute(DELETAR_PACIENTE, (id,))                
                messagebox.showinfo("Sucesso", f"Paciente '{name}' excluído com sucesso.")
                self.get(tree)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao excluir paciente: {e}")
                
    def update(self, tree: ttk.Treeview):
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Aviso", "Selecione um paciente para editar.")
                return
            
            id = tree.item(selected[0])['values'][0]
            db = Database("sono.db")
            db.execute(BUSCAR_POR_ID, (id,))    
            
    def save(self, entries, id):
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
                "dist_sono": entries[Field.DIST_SONO].get()
            }
            db = Database("sono.db")
            db.execute(UPDATE_PACIENTE, (*data.values(), id))
            return True
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar alterações: {e}")
            return False
        
    def get_ocupations(self):
        db = Database("sono.db")
        rows = db.fetchall(SELECIONAR_OCUPACOES)
        occupations = [row[0] for row in rows]
        db.close()
        return occupations

            
            