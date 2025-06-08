from services.database.queries import *

class ConsoleTest:
    def __init__(self):
        self = None
        
    def insert_pacient(self, db):
        nome = input("Nome: ")
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

        dados = (nome, idade, genero, ocupacao, duracao, qualidade, atividade, passos, bmi, estresse, fc, dist)
        db.execute(INSERIR_PACIENTE, dados)
        print("Paciente inserido com sucesso.\n")
        
    def atualizar_paciente(db):
        id_paciente = int(input("ID do paciente a atualizar: "))
        nova_qualidade = int(input("Nova qualidade de sono (1-10): "))
        db.execute(ATUALIZAR_QUALIDADE_SONO, (nova_qualidade, id_paciente))
        print("Atualizado com sucesso.\n")
        
    def deletar_paciente(db):
        id_paciente = int(input("ID do paciente a deletar: "))
        db.execute(DELETAR_PACIENTE, (id_paciente,))
        print("Deletado com sucesso.\n")
    
    def listar_pacientes(db):
        pacientes = db.fetchall(LISTAR_PACIENTES)
        for p in pacientes:
            print(p)
            
    
    def consultar_por_ocupacao(db):
        ocupacao = input("Digite a ocupação: ")
        resultados = db.fetchall(CONSULTAR_POR_OCUPACAO, (ocupacao,))
        for r in resultados:
            print(r)
            
    def consultar_disturbio(db):
        dist = input("Digite o distúrbio (None, Insomnia, Sleep Apnea): ")
        resultados = db.fetchall(CONSULTAR_DISTURBIO, (dist,))
        for r in resultados:
            print(r)

    def estatisticas_gerais(db):
        total, media_sono, media_qualidade = db.fetchall(ESTATISTICAS_GERAIS)[0]
        print(f"Total de pacientes: {total}")
        print(f"Média de duração do sono: {media_sono:.2f}h")
        print(f"Média de qualidade do sono: {media_qualidade:.2f}")

        dist, qtd = db.fetchall(DISTURBIO_MAIS_COMUM)[0]
        print(f"Distúrbio mais comum: {dist} ({qtd} casos)\n")

    def medias_por_categoria(pd, db):
        df = pd.read_sql_query(SELECIONAR_TODOS_PACIENTES, db.conn)
        df['dist_sono'] = df['dist_sono'].fillna('None')
        print("\nMédia por Categoria de IMC:")
        print(df.groupby('categoria_bmi')[['duracao_sono', 'qualidade_sono']].mean())
        print("\nMédia por Ocupação:")
        print(df.groupby('ocupacao')[['duracao_sono', 'qualidade_sono']].mean())
        print("\nMédia por Distúrbio do Sono:")
        print(df.groupby('dist_sono')[['duracao_sono', 'qualidade_sono']].mean())
        
    def buscar_por_id(db):
        id_paciente = input("Digite o ID: ")
        paciente = db.fetchall(BUSCAR_POR_ID, (id_paciente,))
        print(paciente[0] if paciente else "Paciente não encontrado.")
        
    def menu(self, import_csv, exportar_para_csv, simular_sono, backup_banco, pd, db):
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
            if opcao == '1': ConsoleTest().insert_pacient(db)
            elif opcao == '2': import_csv(input("Caminho do arquivo CSV: "))
            elif opcao == '3': ConsoleTest().atualizar_paciente(db)
            elif opcao == '4': ConsoleTest().deletar_paciente(db)
            elif opcao == '5': ConsoleTest().listar_pacientes(db)
            elif opcao == '6': ConsoleTest().consultar_por_ocupacao(db)
            elif opcao == '7': ConsoleTest().consultar_disturbio(db)
            elif opcao == '8': ConsoleTest().estatisticas_gerais(db)
            elif opcao == '10': exportar_para_csv()
            elif opcao == '11': ConsoleTest().buscar_paciente_por_id(db)
            elif opcao == '12': simular_sono()
            elif opcao == '13': backup_banco()
            elif opcao == '0': print("Encerrando o sistema."); break
            else: print("Opção inválida. Tente novamente.")
            
    