import re
from collections import defaultdict

def read_insert_sql(file_path):
    pattern = re.compile(
        r"INSERT INTO consulta \((.*?)\) VALUES\s*(.*?);",
        re.IGNORECASE | re.DOTALL
    )
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    matches = pattern.findall(content)
    columns = [col.strip() for col in matches[0][0].split(',')]
    values = re.findall(r"\((.*?)\)", matches[0][1])

    consultas = []
    for value in values:
        consulta_values = [val.strip().strip("'") for val in value.split(',')]
        consultas.append(dict(zip(columns, consulta_values)))
    
    return consultas

def verify_consultas(consultas):
    # Dicionários para armazenar ocorrências de consultas por paciente e por médico
    consultas_por_paciente = defaultdict(list)
    consultas_por_medico = defaultdict(list)

    for consulta in consultas:
        chave_paciente = (consulta['ssn'], consulta['data'], consulta['hora'])
        chave_medico = (consulta['nif'], consulta['data'], consulta['hora'])
        
        consultas_por_paciente[chave_paciente].append(consulta)
        consultas_por_medico[chave_medico].append(consulta)
    
    # Verificar consultas duplicadas para pacientes
    duplicados_pacientes = [chave for chave, ocorrencias in consultas_por_paciente.items() if len(ocorrencias) > 1]
    # Verificar consultas duplicadas para médicos
    duplicados_medicos = [chave for chave, ocorrencias in consultas_por_medico.items() if len(ocorrencias) > 1]
    
    return duplicados_pacientes, duplicados_medicos

# Ler o arquivo de inserção de consultas
consultas = read_insert_sql('insert_consultas.sql')

# Verificar duplicatas
duplicados_pacientes, duplicados_medicos = verify_consultas(consultas)

# Exibir resultados
if duplicados_pacientes:
    print("Pacientes com consultas duplicadas (mesma data e hora):")
    for dup in duplicados_pacientes:
        print(f"Paciente SSN: {dup[0]}, Data: {dup[1]}, Hora: {dup[2]}")
else:
    print("Nenhum paciente com consultas duplicadas encontrado.")

if duplicados_medicos:
    print("Médicos com consultas duplicadas (mesma data e hora):")
    for dup in duplicados_medicos:
        print(f"Médico NIF: {dup[0]}, Data: {dup[1]}, Hora: {dup[2]}")
else:
    print("Nenhum médico com consultas duplicadas encontrado.")
