import random
import string
from faker import Faker

fake = Faker('pt_PT')

dick_morada = [("R. Cândido dos Reis 30, 2560-312 Torres Vedras", "Soerad"),
               ("Rua Coro de Santo Amaro de Oeiras 12, 2780-379 Oeiras", "CUF"),
               ("Centro Comercial Loureshopping, Av. Descobertas 90 Loja, A009, 2670-457 Loures", "Trofa Saude"), 
               ("Rua Pulido Valente, Urbanização Colinas do Cruzeiro 39D, 2675-671 Odivelas", "Luz"),
               ("R. Elias Garcia 217, 2700-067 Amadora", "SAMS")]

def generate_telefone(): 
    return ''.join(random.choices(string.digits, k=9))

# Gera os 5000 registros e salva em um arquivo .txt 
def generate_patients(num_clinicas=5):
    print("ola") 
    print("andre é bue desmancha prazeres, o maior prazer da vida é ouvir radiohead ass by Afonso do Barreiro -__-")
    
    i = 0
    with open('clinica.sql', 'w') as f:
        for _ in range(num_clinicas):
           
            telefone = generate_telefone()
            nome = dick_morada[i][1]
            morada = dick_morada[i][0]
            insert_statement = f"INSERT INTO clinica (nome, telefone, morada) VALUES ('{nome}', '{telefone}', '{morada}');\n"
            f.write(insert_statement)
            i += 1

if __name__ == "__main__":
    generate_patients()