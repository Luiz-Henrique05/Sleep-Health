from enum import Enum

class Field(Enum):
    NOME = "Nome"
    IDADE = "Idade"
    GENERO = "Gênero"
    OCUPACAO = "Ocupação"
    DURACAO_SONO = "Duração do Sono (h)"
    QUALIDADE_SONO = "Qualidade do Sono"
    ATIVIDADE_FISICA = "Atividade Física"
    PASSOS_DIARIOS = "Passos Diários"
    CATEGORIA_BMI = "Categoria de IMC"
    NIVEL_ESTRESSE = "Nível de Estresse"
    FREQUENCIA_CARDIACA = "Frequência Cardíaca"
    DIST_SONO = "Distúrbio do Sono"

FIELD_TYPES = {
    Field.GENERO: {"type": "combo", "values": ["Masculino", "Feminino", "Outro"]},
    Field.QUALIDADE_SONO: {"type": "combo", "values": ["Muito Baixa", "Baixa", "Média", "Alta", "Muito Alta"]},
    Field.ATIVIDADE_FISICA: {"type": "combo", "values": ["Sedentário", "Moderado", "Intensivo", "Extremamente Intensivo"]},
    Field.CATEGORIA_BMI: {"type": "combo", "values": ["Abaixo do Peso", "Peso Normal", "Sobrepeso", "Obesidade Leve", "Obesidade Moderada", "Obesidade Severa"]},
    Field.NIVEL_ESTRESSE: {"type": "combo", "values": ["Muito Baixa", "Baixa", "Média", "Alta", "Muito Alta"]},
}

QUALIDADE_SONO_MAP = {
    "Muito Baixa": 1,
    "Baixa": 3,
    "Média": 5,
    "Alta": 7,
    "Muito Alta": 10
}
ATIVIDADE_FISICA_MAP = {
    "Sedentário": 0,
    "Moderado": 30,
    "Intensivo": 60,
    "Extremamente Intensivo": 100
}
STRESS_MAP = {
    "Muito Baixa": 1,
    "Baixa": 3,
    "Média": 5,
    "Alta": 7,
    "Muito Alta": 10
}

CATEGORIA_BMI_MAP = {
    "Abaixo do Peso": "Abaixo do Peso",
    "Peso Normal": "Peso Normal",
    "Sobrepeso": "Sobrepeso",
    "Obesidade Leve": "Obesidade Leve",
    "Obesidade Moderada": "Obesidade Moderada",
    "Obesidade Severa": "Obesidade Severa"
}