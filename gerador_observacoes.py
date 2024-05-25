import random
import re

# Function to read data from SQL file
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

# Parameters for symptoms and metrics observations
symptoms_parameters = [
    "Dor de cabeça", "Tontura", "Náusea", "Vômito", "Febre", "Tosse",
    "Dor abdominal", "Dor nas costas", "Dor no peito", "Dor nas articulações",
    "Fadiga", "Perda de apetite", "Inchaço", "Falta de ar", "Sangramento", "Dor de Garganta",
    "Dor muscular", "Dor nos olhos", "Sensação de queimação", "Sensação de formigueiro", 
    "Dormência", "Vertigem", "Constipação", "Diarreia", "Ardor ao urinar", "Sensação de peso no estômago",
    "Sensação de aperto no peito", "Sensação de desmaio", "Sensação de coceira", "Sensação de pressão no ouvido",
    "Desconforto ao engolir", "Sensação de gases", "Sensação de rigidez muscular", "Sensação de calor excessivo",
    "Sensação de frio intenso", "Sensação de rigidez nas articulações", "Sensação de rigidez no pescoço",
    "Sensação de pulsação nas têmporas", "Sensação de perda de equilíbrio", "Sensação de estar sob pressão",
    "Sensação de mal-estar geral", "Sensação de pontadas", "Sensação de peso nos membros",
    "Sensação de queimação ao urinar", "Sensação de bater do coração", "Sensação de garganta fechada",
    "Sensação de pele arrepiada", "Sensação de cansaço extremo", "Dor na Lingua", "Dor de Cotovelo (Sportinguismus)"
]

metrics_parameters = [
    "Pressão arterial", "Temperatura corporal", "Peso", "Altura", "Frequência cardíaca",
    "Nível de glicose", "Nível de colesterol", "Hemoglobina", "Saturação de oxigênio",
    "Índice de massa corporal (IMC)", "Obesidade", "Autismo", "Demencia", "Diarreia", "Loucura",
    "Estigmatismo", "Miopia", "Taxa de Ferro no Sangue", "Taxa de Alcool", "Taxa de THC no sangue"
]

# Function to generate random observations for a consultation
def generate_observations(consultation_id):
    num_symptoms = random.randint(1, 5)
    num_metrics = random.randint(0, 3)

    symptoms = random.sample(symptoms_parameters, num_symptoms)
    metrics = random.sample(metrics_parameters, num_metrics)

    observations = []
    for symptom in symptoms:
        observations.append((consultation_id, symptom, None))

    for metric in metrics:
        value = round(random.uniform(1, 10), 1)  # Random float value
        observations.append((consultation_id, metric, value))

    return observations

# Read consultations data from SQL file
consultations_data = read_data_from_sql('insert_consultas.sql', 'consulta')

# Generate and write observations INSERT statements to a file
with open('observacao.sql', 'w', encoding='utf-8') as f:
    for consulta in consultations_data:
        consultation_id = consulta['id']
        observations = generate_observations(consultation_id)
        
        for observation in observations:
            id, parametro, valor = observation
            if valor is not None:
                f.write(f"INSERT INTO observacao (id, parametro, valor) VALUES ({id}, '{parametro}', {valor});\n")
            else:
                f.write(f"INSERT INTO observacao (id, parametro) VALUES ({id}, '{parametro}');\n")

print("Arquivo 'observacoes.sql' gerado com sucesso!")
