CREATE_USUARIOS = """
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    senha TEXT
)
"""

CREATE_PACIENTES = """
CREATE TABLE IF NOT EXISTS pacientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    idade INTEGER,
    genero TEXT,
    ocupacao TEXT,
    duracao_sono REAL,
    qualidade_sono INTEGER,
    atividade_fisica INTEGER,
    passos_diarios INTEGER,
    categoria_bmi TEXT,
    nivel_estresse INTEGER,
    frequencia_cardiaca INTEGER,
    dist_sono TEXT
)
"""

INSERIR_PACIENTE = """
INSERT INTO pacientes (
    nome, idade, genero, ocupacao, duracao_sono, qualidade_sono,
    atividade_fisica, passos_diarios, categoria_bmi, nivel_estresse,
    frequencia_cardiaca, dist_sono
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""

ATUALIZAR_QUALIDADE_SONO = """
UPDATE pacientes SET qualidade_sono = ? WHERE id = ?
"""

DELETAR_PACIENTE = """
DELETE FROM pacientes WHERE id = ?
"""

LISTAR_PACIENTES = """
SELECT * FROM pacientes
"""

CONSULTAR_POR_OCUPACAO = """
SELECT * FROM pacientes WHERE ocupacao = ?
"""

CONSULTAR_DISTURBIO = """
SELECT * FROM pacientes WHERE dist_sono = ?
"""

ESTATISTICAS_GERAIS = """
SELECT COUNT(*), AVG(duracao_sono), AVG(qualidade_sono) FROM pacientes
"""

DISTURBIO_MAIS_COMUM = """
SELECT dist_sono, COUNT(*) FROM pacientes GROUP BY dist_sono ORDER BY COUNT(*) DESC LIMIT 1
"""

BUSCAR_POR_ID = """
SELECT * FROM pacientes WHERE id = ?
"""

SELECIONAR_PACIENTES_POR_DISTURBIO = """
SELECT * FROM pacientes WHERE dist_sono = ?
"""

SELECIONAR_TODOS_PACIENTES = """
SELECT * FROM pacientes
"""

SELECIONAR_PACIENTE_EDIT = """
SELECT id, nome, idade, genero, dist_sono FROM pacientes
"""

UPDATE_PACIENTE = """
    UPDATE pacientes SET
        nome = ?,
        idade = ?,
        genero = ?,
        ocupacao = ?,
        duracao_sono = ?,
        qualidade_sono = ?,
        atividade_fisica = ?,
        passos_diarios = ?,
        categoria_bmi = ?,
        nivel_estresse = ?,
        frequencia_cardiaca = ?,
        dist_sono = ?
    WHERE id = ?
"""

SELECIONAR_OCUPACOES = """
SELECT DISTINCT ocupacao FROM pacientes
"""