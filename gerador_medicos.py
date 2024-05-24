from faker import Faker
import random

# Inicializa o Faker
fake = Faker('pt_PT')

# Define o número de médicos e especialidades
num_clinica_geral = 20
num_outros_medicos = 40
especialidades = ['ortopedia', 'cardiologia', 'dermatologia', 'neurologia', 'gastroenterologia']

# Função para gerar um NIF válido (9 dígitos)
def generate_nif():
    return ''.join([str(random.randint(0, 9)) for _ in range(9)])

# Função para gerar um número de telefone válido (9 a 15 dígitos)
def generate_telefone():
    return ''.join([str(random.randint(0, 9)) for _ in range(random.randint(9, 9))])

# Gera os médicos
medicos = []

# Gera médicos de clínica geral
for _ in range(num_clinica_geral):
    medico = {
        'nif': generate_nif(),
        'nome': fake.unique.name(),
        'telefone': generate_telefone(),
        'morada': fake.address().replace('\n', ', '),
        'especialidade': 'clínica geral'
    }
    medicos.append(medico)

# Gera médicos de outras especialidades
for _ in range(num_outros_medicos):
    especialidade = random.choice(especialidades)
    medico = {
        'nif': generate_nif(),
        'nome': fake.unique.name(),
        'telefone': generate_telefone(),
        'morada': fake.address().replace('\n', ', '),
        'especialidade': especialidade
    }
    medicos.append(medico)

# Gera os comandos SQL para inserir os médicos na tabela e escreve em um arquivo .txt
with open('medicos.txt', 'w') as file:
    for medico in medicos:
        sql_command = f"INSERT INTO medico (nif, nome, telefone, morada, especialidade) VALUES ('{medico['nif']}', '{medico['nome']}', '{medico['telefone']}', '{medico['morada']}', '{medico['especialidade']}');\n"
        file.write(sql_command)

print("Dados dos médicos foram gerados e salvos em medicos.txt")
