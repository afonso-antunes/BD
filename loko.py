import re

def extrair_nifs(filename, table):
    nifs = set()
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith(f"INSERT INTO {table}"):
                # Extrai o NIF usando uma expressão regular
                nif = re.search(r"VALUES\s*\(\s*'(\d{9})'", line)
                if nif:
                    nifs.add(nif.group(1))
    return nifs

# Arquivos de entrada
arquivo_medicos = 'medicos.txt'
arquivo_pacientes = 'populate.sql'
arquivo_enfermeiros = 'enfermeiros.txt'

# Extrai os NIFs dos médicos e dos pacientes
nifs_medicos = extrair_nifs(arquivo_medicos, 'medico')
nifs_pacientes = extrair_nifs(arquivo_pacientes, 'paciente')
nifs_enfermeiros = extrair_nifs(arquivo_enfermeiros, 'enfermeiro')

# Encontra os NIFs comuns
nifs_comuns = nifs_medicos.intersection(nifs_pacientes)

# Imprime os resultados
if nifs_comuns:
    print("NIFs comuns encontrados:")
    for nif in nifs_comuns:
        print(nif)
else:
    print("Nenhum NIF comum encontrado.")
