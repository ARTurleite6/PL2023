from math import inf

class Person:
    def __init__(self, idade, sexo, tensao, colesterol, batimento, temDoenca):
        self.idade = idade
        self.sexo = sexo
        self.tensao = tensao
        self.colesterol = colesterol
        self.batimento = batimento
        self.temDoenca = temDoenca

    def __str__(self):
        return f"Idade: {self.idade}, Sexo: {self.sexo}, Tensao: {self.tensao}, Colesterol: {self.colesterol}, Batimento: {self.batimento}, Tem Doenca: {self.temDoenca}"

def read_file(file):
    data = []
    greater_age = 0
    greater_colesterol = 0
    minor_colesterol = inf
    with open(file, 'r') as f:
        f.readline() # first line
        for line in f:
            line = line.rstrip().split(',')
            person = Person(int(line[0]), line[1], int(line[2]), int(line[3]), int(line[4]), True if line[5] == "1" else False)
            data.append(person)
            if(person.idade > greater_age):
                greater_age = person.idade
            if(person.colesterol > greater_colesterol):
                greater_colesterol = person.colesterol
            if(person.colesterol < minor_colesterol):
                minor_colesterol = person.colesterol
            
    return data, greater_age, greater_colesterol, minor_colesterol
            
def rate_doenca_sexo(data):
    total = len(data)
    masc, fem = 0, 0
    masc, fem = list(filter(lambda x: x.sexo == 'M' and x.temDoenca, data)), list(filter(lambda y: y.sexo == 'F' and y.temDoenca, data))
    return {"Masculino": len(masc)/total, "Feminino": len(fem)/total}

def rate_doenca_idade(data, limite_idade):
    min_age = 30
    max_age = limite_idade
    age_ranges = {}
    age_array_size = 4
    for age in range(min_age, max_age + 1, age_array_size):
        age_ranges[f"[{age}-{age + age_array_size}]"] = 0

    for person in data:
        for age_range in age_ranges.keys():
            start, end = map(int, age_range[1:-1].split('-'))
            if person.temDoenca and person.idade >= start and person.idade <= end:
                age_ranges[age_range] += 1
                break

    return age_ranges

def rate_doenca_colesterol(data, limite_sup_colesterol, limite_inf_colesterol):
    min = limite_inf_colesterol
    max = limite_sup_colesterol
    array_range_size = 10
    colesterol_ranges = {}
    for colesterol in range(min, max + 1, 10):
        colesterol_ranges[f"[{colesterol}-{colesterol + array_range_size}]"] = 0

    for person in data:
        for colesterol_range in colesterol_ranges.keys():
            start, end = map(int, colesterol_range[1:-1].split('-'))
            if person.temDoenca and person.colesterol >= start and person.colesterol <= end:
                colesterol_ranges[colesterol_range] += 1
                break
    return colesterol_ranges

def get_tabela(distribuicao):
    res = ""
    for key, value in distribuicao.items():
        res += f"{key: ^20} | {value: ^20}\n"
    return res

def main():
    data, limite_idade, limite_sup_colesterol, limite_inf_colesterol = read_file('myheart.csv')
    distribuicoes = {1: rate_doenca_sexo(data), 2: rate_doenca_idade(data, limite_idade), 3: rate_doenca_colesterol(data, limite_sup_colesterol, limite_inf_colesterol)}
    escolha = 1
    while escolha != 0:
        escolha = int(input("Qual distribuicao deseja visualizar: \n1 - Sexo\n2 - Idade\n3 - Colesterol\n0- Sair: "))
        if escolha != 0:
            distribuicao = distribuicoes[escolha]
            print(get_tabela(distribuicao))

if __name__ == "__main__":
    main()
