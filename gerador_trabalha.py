import random
import re
from collections import defaultdict

# Arquivo de entrada
arquivo_medicos = 'medicos.sql'

# Define as clínicas
clinicas = ["Soerad", "CUF", "Trofa Saude", "Luz", "SAMS"]

# Dias da semana: 0=domingo, 1=segunda-feira, ..., 6=sábado
dias_da_semana = list(range(7))

# Função para extrair NIFs dos médicos do arquivo
def extrair_medicos(filename):
    medicos = []
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith("INSERT INTO medico"):
                nif = re.search(r"VALUES\s*\(\s*'(\d{9})'", line)
                if nif:
                    medicos.append(nif.group(1))
    return medicos

# Extrai os médicos do arquivo
medicos = extrair_medicos(arquivo_medicos)

# Dicionário para armazenar a distribuição de médicos por clínica e dia da semana
distribuicao = defaultdict(lambda: defaultdict(list))

# Aloca cada médico em pelo menos duas clínicas diferentes ao longo da semana
for medico in medicos:
    dias_trabalhados = set()
    clinicas_escolhidas = random.sample(clinicas, 2)
    
    for clinica in clinicas_escolhidas:
        dias_clinica = random.sample(dias_da_semana, 2)
        for dia in dias_clinica:
            if len(dias_trabalhados) < 7:
                distribuicao[clinica][dia].append(medico)
                dias_trabalhados.add(dia)

# Verifica e ajusta a distribuição para garantir pelo menos 8 médicos por clínica por dia
for clinica in clinicas:
    for dia in dias_da_semana:
        while len(distribuicao[clinica][dia]) < 8:
            medico_adicional = random.choice(medicos)
            # Certifica-se de que o médico adicional não está escalado para outra clínica no mesmo dia
            if not any(medico_adicional in distribuicao[outra_clinica][dia] for outra_clinica in clinicas):
                distribuicao[clinica][dia].append(medico_adicional)

# Gera os comandos SQL para inserir na tabela trabalha
with open('trabalha.txt', 'w') as file:
    for clinica in clinicas:
        for dia in dias_da_semana:
            for medico in distribuicao[clinica][dia]:
                sql_command = f"INSERT INTO trabalha (nif, nome, dia_da_semana) VALUES ('{medico}', '{clinica}', {dia});\n"
                file.write(sql_command)

print("Dados de trabalho dos médicos foram gerados e salvos em trabalha.txt")