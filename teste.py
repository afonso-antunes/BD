import random
from datetime import date, timedelta, time
import re

def generate_random_time():
    return time(hour=random.randint(8, 17), minute=random.choice([0, 30]))

# Helper function to write data to a file
def write_to_file(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(data)

# Read data from SQL files
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

clinicas = read_data_from_sql('sqlFiles/clinicas.sql', 'clinica')
medicos = read_data_from_sql('sqlFiles/medico.sql', 'medico')
pacientes = read_data_from_sql('sqlFiles/populate.sql', 'paciente')
trabalha = read_data_from_sql('sqlFiles/trabalha.sql', 'trabalha')

# Get all unique days in 2023 and 2024
start_date = date(2023, 1, 1)
end_date = date(2024, 12, 31)
delta = end_date - start_date
all_dates = [start_date + timedelta(days=i) for i in range(delta.days + 1)]

# Ensure every patient has at least one consultation
consultations = []
sns_counter = 100000000000

for patient in pacientes:
    ssn = patient['ssn']
    consultation_date = random.choice(all_dates)
    consultation_time = generate_random_time()
    doctor = random.choice(medicos)
    clinic = random.choice(clinicas)
    sns_code = str(sns_counter)
    consultations.append({
        'ssn': ssn,
        'nif': doctor['nif'],
        'nome': clinic['nome'],
        'data': consultation_date,
        'hora': consultation_time,
        'codigo_sns': sns_code
    })
    sns_counter += 1

# Ensure each day has at least 20 consultations per clinic
for clinic in clinicas:
    for single_date in all_dates:
        for _ in range(20):
            ssn = random.choice(pacientes)['ssn']
            doctor = random.choice(medicos)
            consultation_time = generate_random_time()
            sns_code = str(sns_counter)
            consultations.append({
                'ssn': ssn,
                'nif': doctor['nif'],
                'nome': clinic['nome'],
                'data': single_date,
                'hora': consultation_time,
                'codigo_sns': sns_code
            })
            sns_counter += 1

# Ensure each doctor has at least 2 consultations per day
for doctor in medicos:
    for single_date in all_dates:
        for _ in range(2):
            ssn = random.choice(pacientes)['ssn']
            clinic = random.choice(clinicas)
            consultation_time = generate_random_time()
            sns_code = str(sns_counter)
            consultations.append({
                'ssn': ssn,
                'nif': doctor['nif'],
                'nome': clinic['nome'],
                'data': single_date,
                'hora': consultation_time,
                'codigo_sns': sns_code
            })
            sns_counter += 1

# Create SQL insert statements
sql_inserts = []
for consultation in consultations:
    sql_inserts.append(
        f"INSERT INTO consulta (ssn, nif, nome, data, hora, codigo_sns) VALUES "
        f"('{consultation['ssn']}', '{consultation['nif']}', '{consultation['nome']}', "
        f"'{consultation['data']}', '{consultation['hora']}', '{consultation['codigo_sns']}');"
    )

# Write to consultas.sql
write_to_file('consultas.sql', '\n'.join(sql_inserts))
