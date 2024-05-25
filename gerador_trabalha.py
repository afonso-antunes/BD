import random
import re
from collections import defaultdict

aux = []

# Arquivo de entrada
arquivo_medicos = 'medico.sql'

# Define as clínicas
clinicas = ["Soerad", "CUF", "Trofa Saude", "Luz", "SAMS"]

# Dias da semana: 0=domingo, 1=segunda-feira, ..., 6=sábado
# Lendo os dados do arquivo medico.sql
with open('sqlFiles/medico.sql', 'r') as file:
    medico_lines = file.readlines()

# Lista para armazenar os inserts de trabalha
inserts_trabalha = []

# Lista dos dias da semana
dias_da_semana = list(range(0, 7))    # alterado

# Contador para distribuir médicos em clínicas
clinica_counter = 0

# Percorrendo as linhas do arquivo medico.sql
for line in medico_lines:
    if line.startswith("INSERT INTO medico"):
        # Extraindo os dados do INSERT INTO medico
        parts = line.split("VALUES (")[1].strip().rstrip(');').split(', ')
        
        nif = parts[0].strip("'")
        nome = parts[1].strip("'")
        telefone = parts[2].strip("'")
        morada = parts[3].strip("'")
        especialidade = parts[4].strip("'")
        
        # Distribuindo médicos em clínicas
        for dia in dias_da_semana:
            
            if (nif,dia) in aux: continue
            
            aux.append((nif,dia))
            
            inserts_trabalha.append(
                f"INSERT INTO trabalha (nif, nome, dia_da_semana) VALUES ('{nif}', '{clinicas[clinica_counter]}', {dia});"
            )
        
            # Avançando para a próxima clínica
            clinica_counter = (clinica_counter + 1) % len(clinicas)
            
            # Verificando se a clínica counter voltou ao início
            if clinica_counter == 0:
                clinica_counter += 1  # Evita que o médico trabalhe no mesmo lugar no mesmo dia da semana
            
            

# Escrevendo os INSERTS no arquivo trabalho.sql
with open('sqlFiles/trabalha.sql', 'w') as file:
    for insert in inserts_trabalha:
        file.write(insert + "\n")