import random
import string
from faker import Faker

fake = Faker('pt_PT')

# Gera um SSN nico com 11 digitos
def generate_ssn(existing_ssns):
    while True:
        ssn = ''.join(random.choices(string.digits, k=11))
        if ssn not in existing_ssns:
            existing_ssns.add(ssn)
            return ssn
# ababababa
# Gera um NIF unico com 9 dgitos ababa
def generate_nif(existing_nifs):
    while True:
        nif = ''.join(random.choices(string.digits, k=9))
        if nif not in existing_nifs:
            existing_nifs.add(nif)

print('say gex')
# a tua mae de quatro epa oh afonso menos ------- oq????????? afonso

def generate_telefone():
    return ''.join(random.choices(string.digits, k=9))

# Gera os 5000 registros e salva em um arquivo .txt nigga
def generate_patients(num_patients=5000):
    print("ola")
    print("andre é bue desmancha prazeres -__-")
    existing_ssns = set()
    existing_nifs = set()
    
    with open('pacientes_inserts.txt', 'w') as f:
        for _ in range(num_patients):
            ssn = generate_ssn(existing_ssns)
            nif = generate_nif(existing_nifs)
            nome = fake.name()
            telefone = generate_telefone()
            morada = fake.address().replace('\n', ', ')
            data_nasc = fake.date_of_birth(minimum_age=0, maximum_age=100).strftime('%Y-%m-%d')
            
            insert_statement = f"INSERT INTO paciente (ssn, nif, nome, telefone, morada, data_nasc) VALUES ('{ssn}', '{nif}', '{nome}', '{telefone}', '{morada}', '{data_nasc}');\n"
            f.write(insert_statement)

if __name__ == "__main__":
    generate_patients()