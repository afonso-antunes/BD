
import random
import re
from datetime import date, timedelta, time, datetime
from dataclasses import dataclass

global_id = 0
sns_counter = 100000000000

registo_medico_ocupado = []

@dataclass
class Consulta:
    id: int
    ssn: str
    nif: str
    nome: str
    data: date
    hora: time
    codigo_sns: str
    
# Função para gerar uma data aleatória entre 2023 e 2024 no formato yyyy-mm-DD
def data_aleatoria():
    # Gerar um ano aleatório entre 2023 e 2024
    ano = random.choice([2023, 2024])
    
    # Gerar um dia do ano aleatório entre 1 e 365 (ou 366 para anos bissextos)
    dia_do_ano = random.randint(1, 365 if ano != 2024 else 366)
    
    # Construir a data a partir do ano e do dia do ano
    data = datetime(year=ano, month=1, day=1) + timedelta(days=dia_do_ano - 1)
    
    # Formatar a data no formato yyyy-mm-DD
    data_formatada = data.strftime("%Y-%m-%d")
    
    return data_formatada

# Função para gerar uma hora aleatória com minutos 00 ou 30 no formato HH:mm
def hora_aleatoria():
    # Gerar horas aleatórias entre 00 e 23
    hora = random.randint(0, 23)
    
    # Escolher minutos aleatoriamente entre 0 e 1 (para representar 00 ou 30)
    minutos = random.choice([0, 30])
    
    # Formatar a hora e os minutos no formato HH:mm
    hora_formatada = f"{hora:02}:{minutos:02}"
    
    return hora_formatada
def generate_random_time():
    return time(hour=random.randint(8, 17), minute=random.choice([0, 30]))

def converter_para_data(data_str):
    return datetime.strptime(data_str, "%Y-%m-%d").date()

def write_to_file(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(data)

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


def custom_weekday(date):
    return (date.weekday() + 1) % 7

#print(trabalha)
lista_clinicas_dias = []
lista = []
for medico_line in medicos:
    #print(medico_line)
    nif_medico = medico_line['nif']
    
    for _ in range(2):
        
        global_id += 1
        sns_counter += 1
        for trabalha_line in trabalha:
            
            nif_trabalho = trabalha_line["nif"]
            
            if nif_medico == nif_trabalho:
                dia_de_trabalho_medico = trabalha_line["dia_da_semana"]
                nome_clinica = trabalha_line["nome"]
                break

            
        
        # Gerar data e hora aleatórias
        while True:
            data = data_aleatoria()
            hora = hora_aleatoria()
            print("help")
            print(custom_weekday(converter_para_data(data)), dia_de_trabalho_medico)
            if  (custom_weekday(converter_para_data(data)) == dia_de_trabalho_medico) and \
                ((nif_medico, data, hora) not in registo_medico_ocupado):        # Sair do loop while se a combinação for válida
                break 
            
        registo_medico_ocupado.add((nif_medico, data, hora))
        
        
        nif_paciente = random.choice(list(pacientes.keys()))
        paciente = pacientes[nif_paciente]
        
        ssn_paciente = paciente['ssn']
        
        nova_consulta = Consulta(
            id = global_id,
            ssn = ssn_paciente,
            nif = nif_medico,
            nome = nome_clinica,
            data = data,
            hora = hora,
            codigo_sns = sns_counter
        )
        
print("registo", registo_medico_ocupado)


# Ensure every patient has at least one consultation
consultations = []







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
