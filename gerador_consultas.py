import random
import datetime
import re

# Funções auxiliares para geração de dados
def generate_date(year):
    start_date = datetime.date(year, 1, 1)
    end_date = datetime.date(year, 12, 31)
    return start_date + datetime.timedelta(days=random.randint(0, (end_date - start_date).days))

def generate_time():
    return datetime.time(random.randint(8, 17), random.choice([0, 15, 30, 45]))

def generate_sns_code():
    return ''.join([str(random.randint(0, 9)) for _ in range(12)])

# Função para ler dados dos arquivos SQL
def read_data_from_sql(file_path, table_name):
    pattern = re.compile(
        fr"INSERT INTO {table_name}\s*\((.*?)\)\s*VALUES\s*\((.*?)\);",
        re.IGNORECASE | re.DOTALL
    )
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    matches = pattern.findall(content)
    data = []
    for match in matches:
        columns = [col.strip() for col in match[0].split(',')]
        values = [val.strip().strip("'") for val in match[1].split(',')]
        data.append(dict(zip(columns, values)))
    return data

# Ler dados dos arquivos SQL
clinicas = read_data_from_sql('clinicas.sql', 'clinica')
medicos = read_data_from_sql('medicos.sql', 'medico')
pacientes = read_data_from_sql('populate.sql', 'paciente')

# Número de entidades
num_pacientes = len(pacientes)
num_clinicas = len(clinicas)
num_medicos = len(medicos)

# Número de dias em cada ano
dias_2023 = 365
dias_2024 = 366
total_dias = dias_2023 + dias_2024

# Consultas mínimas por paciente, clínica e médico
consultas_por_pacientes = num_pacientes
consultas_por_clinicas_total = num_clinicas * total_dias * 20
consultas_por_medicos = num_medicos * 2

# Número total de consultas necessário
total_consultas = max(consultas_por_pacientes, consultas_por_clinicas_total, consultas_por_medicos)

print(f"Número total de consultas necessário para 2023 e 2024: {total_consultas}")

# Dicionários para verificar duplicações
consultas_paciente_horario = {}
consultas_medico_horario = {}
consultas_unicas = {}

# Geração de consultas
consultas = []

# Função para verificar duplicidade
def verifica_duplicidade(ssn, nif, date, time):
    if (ssn, date, time) in consultas_paciente_horario:
        return True
    if (nif, date, time) in consultas_medico_horario:
        return True
    if (ssn, nif, date, time) in consultas_unicas:
        return True
    return False

# Garantir consultas por paciente
for paciente in pacientes:
    year = random.choice([2023, 2024])
    date = generate_date(year)
    time = generate_time()
    medico = random.choice(medicos)
    while verifica_duplicidade(paciente['ssn'], medico['nif'], date, time):
        date = generate_date(year)
        time = generate_time()
        medico = random.choice(medicos)
    clinica = random.choice(clinicas)['nome']
    consulta = {
        'ssn': paciente['ssn'],
        'nif': medico['nif'],
        'nome': clinica,
        'data': date,
        'hora': time,
        'codigo_sns': generate_sns_code()
    }
    consultas.append(consulta)
    consultas_paciente_horario[(paciente['ssn'], date, time)] = True
    consultas_medico_horario[(medico['nif'], date, time)] = True
    consultas_unicas[(paciente['ssn'], medico['nif'], date, time)] = True

# Garantir consultas diárias por clínica
for year in [2023, 2024]:
    days_in_year = 365 if year == 2023 else 366
    for clinica in clinicas:
        clinica_nome = clinica['nome']
        for day in range(days_in_year):
            date = datetime.date(year, 1, 1) + datetime.timedelta(days=day)
            for _ in range(20):
                paciente = random.choice(pacientes)
                time = generate_time()
                medico = random.choice(medicos)
                while verifica_duplicidade(paciente['ssn'], medico['nif'], date, time):
                    paciente = random.choice(pacientes)
                    time = generate_time()
                    medico = random.choice(medicos)
                consulta = {
                    'ssn': paciente['ssn'],
                    'nif': medico['nif'],
                    'nome': clinica_nome,
                    'data': date,
                    'hora': time,
                    'codigo_sns': generate_sns_code()
                }
                consultas.append(consulta)
                consultas_paciente_horario[(paciente['ssn'], date, time)] = True
                consultas_medico_horario[(medico['nif'], date, time)] = True
                consultas_unicas[(paciente['ssn'], medico['nif'], date, time)] = True

# Garantir consultas por médico
for medico in medicos:
    for year in [2023, 2024]:
        consultas_medico = [c for c in consultas if c['nif'] == medico['nif'] and c['data'].year == year]
        if len(consultas_medico) < 2:
            needed_consultas = 2 - len(consultas_medico)
            for _ in range(needed_consultas):
                date = generate_date(year)
                time = generate_time()
                paciente = random.choice(pacientes)
                while verifica_duplicidade(paciente['ssn'], medico['nif'], date, time):
                    date = generate_date(year)
                    time = generate_time()
                    paciente = random.choice(pacientes)
                consulta = {
                    'ssn': paciente['ssn'],
                    'nif': medico['nif'],
                    'nome': random.choice(clinicas)['nome'],
                    'data': date,
                    'hora': time,
                    'codigo_sns': generate_sns_code()
                }
                consultas.append(consulta)
                consultas_paciente_horario[(consulta['ssn'], date, time)] = True
                consultas_medico_horario[(consulta['nif'], date, time)] = True
                consultas_unicas[(consulta['ssn'], consulta['nif'], date, time)] = True

# Geração do script SQL para inserção
insert_sql = "INSERT INTO consulta (id, ssn, nif, nome, data, hora, codigo_sns) VALUES\n"
values = []

# Inicialize o valor do ID
next_id = 1

with open('insert_consultas.sql', 'w') as file:
    for consulta in consultas:
        sql_command = f"INSERT INTO consulta (id, ssn, nif, nome, data, hora, codigo_sns) VALUES ('{next_id}', '{consulta['ssn']}', '{consulta['nif']}', '{consulta['nome']}', '{consulta['data']}', '{consulta['hora']}', '{consulta['codigo_sns']}');\n"

        
        # Aumente o valor do ID para o próximo registro
        next_id += 1
        file.write(sql_command)
        





print("Script SQL gerado com sucesso e salvo em 'insert_consultas.sql'")
