# Projeto: Sistema de Análise de Sono com Python e SQLite

Este projeto tem como objetivo armazenar, consultar e analisar dados de pacientes com foco em saúde do sono. Os dados vêm de um dataset real e são tratados por meio de um sistema em Python com SQLite.

---

## ⚙️ Funcionalidades

- Inserção manual de pacientes
- Importação automática do dataset CSV
- Listagem completa dos registros
- Atualização e exclusão de dados (CRUD)
- Consultas por ocupação e distúrbio do sono
- Estatísticas gerais com médias
- Médias agrupadas por categoria (IMC, ocupação, distúrbio)
- Simulador de qualidade de sono (com penalidade por distúrbio)
- Exportação para CSV
- Backup automático do banco

---

## 🧱 Estrutura da Tabela

A tabela `pacientes` contém os seguintes campos:

| Campo                | Tipo     | Descrição                             |
|---------------------|----------|----------------------------------------|
| id                  | INTEGER  | Identificador único                   |
| idade               | INTEGER  | Idade do paciente                     |
| genero              | TEXT     | Gênero (Male/Female)                  |
| ocupacao            | TEXT     | Ocupação profissional                  |
| duracao_sono        | REAL     | Duração média de sono (em horas)       |
| qualidade_sono      | INTEGER  | Qualidade (escala de 1 a 10)           |
| atividade_fisica    | INTEGER  | Nível de atividade física (1 a 100)    |
| nivel_estresse      | INTEGER  | Nível de estresse (1 a 10)             |
| categoria_bmi       | TEXT     | Categoria de IMC                      |
| frequencia_cardiaca | INTEGER  | Batimentos por minuto                  |
| passos_diarios      | INTEGER  | Média de passos por dia                |
| dist_sono           | TEXT     | Distúrbio do sono (None, Insomnia e Sleep Apnea) |

---

## ▶️ Como Executar o Projeto

1. Instale o Python 3: https://python.org
2. Clone o repositório:
```bash
git clone https://github.com/seuusuario/nome-do-repositorio.git
cd nome-do-repositorio
```
3. Instale as dependências:
```bash
pip install -r requirements.txt
```
4. Execute o projeto:
```bash
python main.py
```

---

## 🧪 Dataset Utilizado

- Dataset: `Sleep Health and Lifestyle Dataset`
- Origem: fictícia / acadêmica
- Contém informações de 374 pacientes

---

## 📝 Prints de Funcionamento (sugestão de capturas)

- Menu de navegação
- Consultas filtradas
- Simulação e exportação
- Estatísticas por categoria

---

## 🛠️ Tecnologias

- Python 3
- SQLite (banco local)
- Pandas (manipulação de CSV)
- VS Code (editor sugerido)

---

## ✍️ Autor

Projeto acadêmico desenvolvido por Luiz Henrique
