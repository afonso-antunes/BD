import random
import re

# Função para ler consultas do arquivo SQL
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


# Função para gerar uma lista de medicamentos aleatórios
def generate_medicamentos():
    medicamentos = [
        "Paracetamol", "Ibuprofeno", "Dipirona", "Omeprazol", "Amoxicilina", "Atorvastatina", "Cloridrato de Sertralina",
        "Losartana Potássica", "Rivotril", "Dexametasona", "Ranitidina", "Ciprofloxacino", "Clonazepam", "Sinvastatina",
        "Escitalopram", "Citalopram", "Metformina", "Levotiroxina", "Sinvastatina", "Rosuvastatina", "Furosemida",
        "Insulina", "Lisinopril", "Tramadol", "Venlafaxina", "Levodopa", "Tiotrópio", "Salmeterol", "Glargina",
        "Travatan", "Bimatoprosta", "Carvedilol", "Digoxina", "Varfarina", "Ciclobenzaprina", "Esomeprazol",
        "Cetirizina", "Loratadina", "Fluoxetina", "Trazodona", "Bupropiona", "Duloxetina", "Pregabalina",
        "Metadona", "Codeína", "Morfina", "Oxycodona", "Fentanil", "Hidromorfona"
    ]
    # Retorna uma amostra aleatória de 1 a 6 medicamentos
    return random.sample(medicamentos, k=random.randint(1, 6))

# Função para gerar uma quantidade aleatória entre 1 e 3
def generate_quantidade():
    return random.randint(1, 3)

def generate_receitas_limitado(consultas, total_receitas=64000, percentual=0.8):
    receitas = []
    receitas_geradas = 0
    for consulta in consultas:
        # Verifica se já atingiu o limite de receitas
        if receitas_geradas >= total_receitas:
            break
        # Determina aleatoriamente se a consulta terá uma receita médica associada
        if random.random() < percentual:
            # Gera a lista de medicamentos para a receita
            medicamentos = generate_medicamentos()
            # Gera a quantidade correspondente a cada medicamento
            quantidades = [generate_quantidade() for _ in medicamentos]
            codigo_sns = consulta['codigo_sns'].lstrip("'")
            #print(codigo_sns)
            # Cria uma receita para cada medicamento
            for medicamento, quantidade in zip(medicamentos, quantidades):
                receita = {
                    'codigo_sns': codigo_sns,
                    'medicamento': medicamento,
                    'quantidade': quantidade
                }
                #print(receita)
                receitas.append(receita)
                receitas_geradas += 1
                # Verifica se já atingiu o limite de receitas
                if receitas_geradas >= total_receitas:
                    break
    return receitas

consultas = read_data_from_sql('insert_consultas.sql', 'consulta')

# Gerar receitas médicas limitadas para as consultas
receitas_limitadas = generate_receitas_limitado(consultas)


with open('receitas_limitadas.sql', 'w') as file:
    for receita in receitas_limitadas:
        sql_command = f"INSERT INTO receita (codigo_sns, medicamento, quantidade) VALUES ('{receita['codigo_sns']}', '{receita['medicamento']}', '{receita['quantidade']}');\n"

        
        file.write(sql_command)
        


print("Receitas médicas limitadas geradas e salvas em 'receitas_limitadas.sql'.")
