import re

def read_consultas_from_sql(file_path):
    pattern = re.compile(
        r"INSERT INTO consulta\s*\((.*?)\)\s*VALUES\s*\((.*?)\);",
        re.IGNORECASE | re.DOTALL
    )
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    matches = pattern.findall(content)
    consultas = []
    for match in matches:
        columns = [col.strip() for col in match[0].split(',')]
        values_str = match[1]
        values = re.findall(r"\('([^']*)', '([^']*)', '([^']*)', '([^']*)', '([^']*)', '([^']*)'\)", values_str)
        for value in values:
            consulta = dict(zip(columns, value))
            consultas.append(consulta)
    return consultas

def find_consultas_by_nif_ssn(file_path, nif, ssn):
    consultas = read_consultas_from_sql(file_path)
    filtered_consultas = [consulta for consulta in consultas if consulta['nif'] == nif and consulta['ssn'] == ssn]
    return filtered_consultas

def print_consultas(consultas):
    for consulta in consultas:
        print(f"SSN: {consulta['ssn']}, NIF: {consulta['nif']}, Clínica: {consulta['nome']}, Data: {consulta['data']}, Hora: {consulta['hora']}, Código SNS: {consulta['codigo_sns']}")

if __name__ == "__main__":
    file_path = 'insert_consultas.sql'
    nif = input("Digite o NIF do médico: ")
    ssn = input("Digite o SSN do paciente: ")
    
    consultas = find_consultas_by_nif_ssn(file_path, nif, ssn)
    
    if consultas:
        print("Consultas encontradas:")
        print_consultas(consultas)
    else:
        print("Nenhuma consulta encontrada para o NIF e SSN fornecidos.")
