from services.database.db import Database
from services.database.queries import *
from view.register.controllers import register_controller
from view.login.controllers import login_controller
import pandas as pd
import shutil

db = Database("sono.db")
db.create(CREATE_USUARIOS)
db.create(CREATE_PACIENTES)

login_controller = login_controller.LoginController(None)
def login(username, senha):
    return login_controller.login(username, senha, db.cursor)

register_controller = register_controller.RegisterController(None)
def register(username, senha):
    return register_controller.register(username, senha, db.db, db.cursor)

def import_csv(caminho):
    df = pd.read_csv(caminho)
    for _, row in df.iterrows():
        paciente = (
            row['Name'], row['Age'], row['Gender'], row['Occupation'], row['Sleep Duration'],
            row['Quality of Sleep'], row['Physical Activity Level'], row['Daily Steps'],
            row['BMI Category'], row['Stress Level'], row['Heart Rate'], row['Sleep Disorder']
        )
        db.execute(INSERIR_PACIENTE, paciente)
    print("Importação concluída.\n")

def exportar_para_csv():
    dist = input("Digite o distúrbio a exportar (None, Insomnia, Sleep Apnea): ")
    df = pd.read_sql_query(SELECIONAR_PACIENTES_POR_DISTURBIO, db.db, params=(dist,))
    df.to_csv(f"pacientes_{dist}.csv", index=False)
    print(f"Exportado para pacientes_{dist}.csv\n")

def simular_sono():
    idade = int(input("Idade: "))
    atividade = int(input("Atividade física: "))
    estresse = int(input("Estresse: "))
    dist = input("Distúrbio do Sono (None, Insomnia, Sleep Apnea): ")

    qualidade = 7.0
    if atividade < 30:
        qualidade -= 1
    elif atividade > 60:
        qualidade += 0.5
    if estresse >= 8:
        qualidade -= 1.5
    elif estresse <= 4:
        qualidade += 0.5
    if idade > 50:
        qualidade -= 0.5
    if dist.lower() in ['insomnia', 'sleep apnea']:
        qualidade -= 1
    qualidade = max(1, min(10, qualidade))
    print(f"Qualidade estimada do sono: {qualidade:.1f}/10\n")

def backup_banco():
    shutil.copyfile("sono.db", "sono_backup.db")
    print("Backup criado como sono_backup.db\n")
