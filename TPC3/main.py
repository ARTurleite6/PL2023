import re

def parse_file(file_path):

    regex_str = r"(?P<numero_processo>\d+)::(?P<data>\d{4}-\d{2}-\d{2})::(?P<nome>[\w\s]+)::(?P<pai>[\w\s]+)?::(?P<mae>[\w\s]+)?::(?P<observacoes>.*)?::"

    r1 = re.compile(regex_str) 

    processos = []

    with open(file_path) as file:
        for line in file.readlines():
            match = r1.match(line)
            if match:
                processos.append(match.groupdict())

    return processos

def calculaSeculo(ano):
    if ano < 1000:
        return 1
    else:
        return (ano // 100) + 1

def first_name(nome):
    reg = r"(\w+)\s"
    r = re.compile(reg)

    result = r.match(nome)
    if result:
        return result.group(1)
    else:
        return None

def last_name(nome):
    reg = r"[\w\s]+\s(\w+)"
    r = re.compile(reg)
    result = r.match(nome)
    if result:
        return result.group(1)
    else:
        return None

def minMaxAno(processos):
    min = 9999
    max = 0

    for processo in processos:
        ano = int(processo['data'][:4])
        if ano < min:
            min = ano
        if ano > max:
            max = ano

    return calculaSeculo(min), calculaSeculo(max)

def get_grau(observacao):
    graus = {
"Irmao",
"Tio",
"Sobrinho",
"Primo",
"Irmaos",
"Pai",
"Filho",
"Sobrinhos",
"Avo",
"Neto",
"Tios",
"Filhos",
"Primos",
"Bisavo",
}

    reg = r"\w+,(?P<grau>\w+)"
    r = re.compile(reg)

    result = r.findall(observacao)

    result = list(filter(lambda x: x in graus, result))

    return result

def freqProcessosGrau(processos):
    graus = {}

    for processo in processos:
        observacoes = processo['observacoes']
        graus_processo = get_grau(observacoes)
        for grau in graus_processo:
            if grau not in graus:
                graus[grau] = 0
            graus[grau] += 1
    return graus

def freqProcessosNome(processos):
    seculos = {}

    for processo in processos:
        ano = int(processo['data'][:4])
        seculo = calculaSeculo(ano)
        if seculo not in seculos:
            seculos[seculo] = {}
        indice_nome = f"nome"
        nome = processo[indice_nome]
        if nome is not None:
            primeiro_nome = first_name(nome)
            apelido = last_name(nome)
            if primeiro_nome not in seculos[seculo]:
                seculos[seculo][primeiro_nome] = 0
            if apelido not in seculos[seculo]:
                seculos[seculo][apelido] = 0
            seculos[seculo][primeiro_nome] += 1
            seculos[seculo][apelido] += 1
    return seculos
                


def freqProcessosAno(processos):
    freq = {}
    for processo in processos:
        ano = processo['data'][:4]
        if ano not in freq:
            freq[ano] = 0
        freq[ano] += 1

    return freq

def processo_to_json(processo):
    res = "{\n"

    for camp in processo:
        if camp is not None:
            res += f"\t\"{camp}\": \"{processo[camp]}\",\n"

    return res + "}\n"

def json_convert(out_file_path, processos):
    result = "[\n"
    for processo in processos:
        result += processo_to_json(processo)
    result += "]"

    with open(out_file_path, "w") as file:
        file.write(result)


def main():
    processos = parse_file("processos.txt")
    frequencias_ano = list(freqProcessosAno(processos).items())
    frequencias_ano.sort(key=lambda x: x[0])
    frequencias_nome = list(freqProcessosNome(processos).items())
    frequencias_nome.sort(key=lambda x: x[0])

    frequencias_graus = list(freqProcessosGrau(processos).items())
    frequencias_graus.sort(key=lambda x: x[1], reverse=True)

    choice = -1
    while choice != 0:
        print("1 - Mostrar frequencia de processos por ano")
        print("2 - Mostrar frequencia de processos por seculo")
        print("3 - Mostrar frequencia de graus de parentesco")
        print("4 - Converter primeiros 20 processos para JSON")
        print("0 - Sair")

        choice = int(input("Escolha uma opcao: "))
        if choice == 1:
            for (ano, value) in frequencias_ano:
                print(f"{ano}: {value}")
        elif choice == 2:
            for (seculo, frequencias) in frequencias_nome:
                print(f"Seculo {seculo}")
                frequencias = list(frequencias.items())
                frequencias.sort(key=lambda x: x[1], reverse=True)
                for frequencia in frequencias[:5]:
                    print(f"\t{frequencia[0]}: {frequencia[1]}")
        elif choice == 3:
            for (grau, value) in frequencias_graus:
                print(f"{grau}: {value}")
        elif choice == 4:
            file = input("Nome do ficheiro: ")
            json_convert(file, processos[:20])



if __name__ == "__main__":
    main()
