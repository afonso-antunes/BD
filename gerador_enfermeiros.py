from faker import Faker
import random

# Inicializa o Faker
fake = Faker('pt_PT')

# Define o número de enfermeiros por clínica
num_enfermeiros_min = 5
num_enfermeiros_max = 6

# Define as clínicas
clinicas = [
    ("R. Cândido dos Reis 30, 2560-312 Torres Vedras", "Soerad"),
    ("Rua Coro de Santo Amaro de Oeiras 12, 2780-379 Oeiras", "CUF"),
    ("Centro Comercial Loureshopping, Av. Descobertas 90 Loja, A009, 2670-457 Loures", "Trofa Saude"),
    ("Rua Pulido Valente, Urbanização Colinas do Cruzeiro 39D, 2675-671 Odivelas", "Luz"),
    ("R. Elias Garcia 217, 2700-067 Amadora", "SAMS")
]

# Função para gerar um NIF válido (9 dígitos)
def generate_nif():
    return ''.join([str(random.randint(0, 9)) for _ in range(9)])

# Função para gerar um número de telefone válido (9 dígitos)
def generate_telefone():
    return ''.join([str(random.randint(0, 9)) for _ in range(9)])

# Gera os enfermeiros
enfermeiros = []

for morada, nome_clinica in clinicas:
    num_enfermeiros = random.randint(num_enfermeiros_min, num_enfermeiros_max)
    for _ in range(num_enfermeiros):
        enfermeiro = {
            'nif': generate_nif(),
            'nome': fake.unique.name(),
            'telefone': generate_telefone(),
            'morada': fake.address().replace('\n', ', '),
            'nome_clinica': nome_clinica
        }
        enfermeiros.append(enfermeiro)

# Gera os comandos SQL para inserir os enfermeiros na tabela e escreve em um arquivo .txt
with open('enfermeiro.sql', 'w') as file:
    for enfermeiro in enfermeiros:
        sql_command = f"INSERT INTO enfermeiro (nif, nome, telefone, morada, nome_clinica) VALUES ('{enfermeiro['nif']}', '{enfermeiro['nome']}', '{enfermeiro['telefone']}', '{enfermeiro['morada']}', '{enfermeiro['nome_clinica']}');\n"
        file.write(sql_command)

print("Dados dos enfermeiros foram gerados e salvos em enfermeiros.txt")
