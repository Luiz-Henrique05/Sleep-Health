
import sqlite3
import pandas as pd
import shutil

conexao = sqlite3.connect('sono.db')
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS pacientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    idade INTEGER,
    genero TEXT,
    ocupacao TEXT,
    duracao_sono REAL,
    qualidade_sono INTEGER,
    atividade_fisica INTEGER,
    nivel_estresse INTEGER,
    categoria_bmi TEXT,
    frequencia_cardiaca INTEGER,
    passos_diarios INTEGER,
    dist_sono TEXT
)
""")
conexao.commit()

def inserir_paciente_manual():
    idade = int(input("Idade: "))
    genero = input("Gênero: ")
    ocupacao = input("Ocupação: ")
    duracao = float(input("Duração do Sono (h): "))
    qualidade = int(input("Qualidade do Sono (1-10): "))
    atividade = int(input("Atividade Física: "))
    estresse = int(input("Nível de Estresse (1-10): "))
    bmi = input("Categoria de IMC: ")
    fc = int(input("Frequência Cardíaca: "))
    passos = int(input("Passos Diários: "))
    dist = input("Distúrbio do Sono (None, Insomnia, Sleep Apnea): ")
    cursor.execute("""
    INSERT INTO pacientes (
        idade, genero, ocupacao, duracao_sono, qualidade_sono, atividade_fisica,
        nivel_estresse, categoria_bmi, frequencia_cardiaca, passos_diarios, dist_sono
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (idade, genero, ocupacao, duracao, qualidade, atividade, estresse, bmi, fc, passos, dist))
    conexao.commit()
    print("Paciente inserido com sucesso.\n")

def importar_csv(caminho):
    df = pd.read_csv(caminho)
    for _, row in df.iterrows():
        paciente = (
            row['Age'], row['Gender'], row['Occupation'], row['Sleep Duration'],
            row['Quality of Sleep'], row['Physical Activity Level'], row['Stress Level'],
            row['BMI Category'], row['Heart Rate'], row['Daily Steps'], row['Sleep Disorder']
        )
        cursor.execute("""
        INSERT INTO pacientes (
            idade, genero, ocupacao, duracao_sono, qualidade_sono, atividade_fisica,
            nivel_estresse, categoria_bmi, frequencia_cardiaca, passos_diarios, dist_sono
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, paciente)
    conexao.commit()
    print("Importação concluída.\n")

def atualizar_paciente():
    id_paciente = int(input("ID do paciente a atualizar: "))
    nova_qualidade = int(input("Nova qualidade de sono (1-10): "))
    cursor.execute("UPDATE pacientes SET qualidade_sono = ? WHERE id = ?", (nova_qualidade, id_paciente))
    conexao.commit()
    print("Atualizado com sucesso.\n")

def deletar_paciente():
    id_paciente = int(input("ID do paciente a deletar: "))
    cursor.execute("DELETE FROM pacientes WHERE id = ?", (id_paciente,))
    conexao.commit()
    print("Deletado com sucesso.\n")

def listar_pacientes():
    cursor.execute("SELECT * FROM pacientes")
    for p in cursor.fetchall():
        print(p)

def consultar_por_ocupacao():
    ocupacao = input("Digite a ocupação: ")
    cursor.execute("SELECT * FROM pacientes WHERE ocupacao = ?", (ocupacao,))
    for r in cursor.fetchall():
        print(r)

def consultar_disturbio():
    dist = input("Digite o distúrbio (None, Insomnia, Sleep Apnea): ")
    cursor.execute("SELECT * FROM pacientes WHERE dist_sono = ?", (dist,))
    for r in cursor.fetchall():
        print(r)

def estatisticas_gerais():
    cursor.execute("SELECT COUNT(*), AVG(duracao_sono), AVG(qualidade_sono) FROM pacientes")
    total, media_sono, media_qualidade = cursor.fetchone()
    print(f"Total de pacientes: {total}")
    print(f"Média de duração do sono: {media_sono:.2f}h")
    print(f"Média de qualidade do sono: {media_qualidade:.2f}")
    cursor.execute("SELECT dist_sono, COUNT(*) FROM pacientes GROUP BY dist_sono ORDER BY COUNT(*) DESC LIMIT 1")
    dist, qtd = cursor.fetchone()
    print(f"Distúrbio mais comum: {dist} ({qtd} casos)\n")

def medias_por_categoria():
    df = pd.read_sql_query("SELECT * FROM pacientes", conexao)
    df['dist_sono'] = df['dist_sono'].fillna('None')
    print("\nMédia por Categoria de IMC:")
    print(df.groupby('categoria_bmi')[['duracao_sono', 'qualidade_sono']].mean())
    print("\nMédia por Ocupação:")
    print(df.groupby('ocupacao')[['duracao_sono', 'qualidade_sono']].mean())
    print("\nMédia por Distúrbio do Sono:")
    print(df.groupby('dist_sono')[['duracao_sono', 'qualidade_sono']].mean())


def exportar_para_csv():
    dist = input("Digite o distúrbio a exportar (None, Insomnia, Sleep Apnea): ")
    df = pd.read_sql_query("SELECT * FROM pacientes WHERE dist_sono = ?", conexao, params=(dist,))
    df.to_csv(f"pacientes_{dist}.csv", index=False)
    print(f"Exportado para pacientes_{dist}.csv\n")

def buscar_por_id():
    id_paciente = input("Digite o ID: ")
    cursor.execute("SELECT * FROM pacientes WHERE id = ?", (id_paciente,))
    paciente = cursor.fetchone()
    print(paciente if paciente else "Paciente não encontrado.")

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
    if dist.lower() in ['insomnia','sleep apnea']:
        qualidade -= 1
    qualidade = max(1, min(10, qualidade))
    print(f"Qualidade estimada do sono: {qualidade:.1f}/10\n")

def backup_banco():
    shutil.copyfile("sono.db", "sono_backup.db")
    print("Backup criado como sono_backup.db\n")

def menu():
    while True:
        print("""
=== MENU ===
1. Inserir paciente manualmente
2. Importar pacientes de CSV
3. Atualizar qualidade do sono
4. Deletar paciente
5. Listar todos os pacientes
6. Consultar por ocupação
7. Consultar por distúrbio do sono
8. Ver estatísticas gerais
9. Ver médias por categoria
10. Exportar pacientes com distúrbio para CSV
11. Buscar paciente por ID
12. Simular qualidade de sono
13. Criar backup do banco
0. Sair
""")
        opcao = input("Escolha uma opção: ")
        if opcao == '1': inserir_paciente_manual()
        elif opcao == '2': importar_csv(input("Caminho do arquivo CSV: "))
        elif opcao == '3': atualizar_paciente()
        elif opcao == '4': deletar_paciente()
        elif opcao == '5': listar_pacientes()
        elif opcao == '6': consultar_por_ocupacao()
        elif opcao == '7': consultar_disturbio()
        elif opcao == '8': estatisticas_gerais()
        elif opcao == '9': medias_por_categoria()
        elif opcao == '10': exportar_para_csv()
        elif opcao == '11': buscar_por_id()
        elif opcao == '12': simular_sono()
        elif opcao == '13': backup_banco()
        elif opcao == '0': print("Encerrando o sistema."); break
        else: print("Opção inválida. Tente novamente.")

if __name__ == '__main__':
    menu()
