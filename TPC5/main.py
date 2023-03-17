import re

class InvalidNumber(Exception):
    pass

class SaldoInsuficiente(Exception):
    pass

levantar_regex = re.compile(r"LEVANTAR")
pousar_regex = re.compile(r"POUSAR")
abortar_regex = re.compile(r"ABORTAR")
moedas_regex = re.compile(r"MOEDA\s+((\d+(?:c|e)(?:,\s*)?)*)")
telefone_regex = re.compile(r"T=(\d{9}|00\d+)")

def get_quantidade_moedas(saldo):
    euros = saldo // 100
    moedas_2_euros = euros // 2
    moedas_1_euro = euros % 2
    resultado = []

    saldo %= 100
    moedas_50_centimos = saldo // 50
    saldo %= 50
    moedas_20_centimos = saldo // 20
    resto = saldo % 20 
    moedas_10_centimos = resto // 10
    resto = resto % 10
    moedas_5_centimos = resto // 5
    moedas_1_centimo = resto % 5

    if moedas_2_euros != 0:
        resultado.append(f"{moedas_2_euros}x2e")
    if moedas_1_euro != 0:
        resultado.append(f"{moedas_1_euro}x1e")
    if moedas_50_centimos != 0:
        resultado.append(f"{moedas_50_centimos}x50c")
    if moedas_20_centimos != 0:
        resultado.append(f"{moedas_20_centimos}x20c")
    if moedas_10_centimos != 0:
        resultado.append(f"{moedas_10_centimos}x10c")
    if moedas_5_centimos != 0:
        resultado.append(f"{moedas_5_centimos}x5c")
    if moedas_1_centimo != 0:
        resultado.append(f"{moedas_1_centimo}x1c")


    return ', '.join(resultado)

def deal_with_moedas(operacao):
    lista_moedas = operacao.group(1)
    moedas = re.findall(r"(\d+(?:c|e))", lista_moedas)

    regex_centimos = re.compile(r"(?P<value>1|5|10|20|50)c")
    regex_euros = re.compile(r"(?P<value>1|2)e")

    saldo_total = 0
    moedas_invalidas = []
    for moeda in moedas:
        centimos = regex_centimos.match(moeda)
        euros = regex_euros.match(moeda)
        if centimos:
            value = int(centimos.group("value"))
            saldo_total += value
        elif euros:
            value = int(euros.group("value"))
            saldo_total += value * 100
        else:
            moedas_invalidas.append(moeda)
    return saldo_total, moedas_invalidas

def get_euros_centimos(saldo):
    euros = saldo // 100
    centimos = saldo % 100
    return euros, centimos

def get_message_moedas(saldo_atual, moedas_invalidas):
        padrao_moeda_invalida = "MOEDA - moeda inválida"
        padrao_saldo = "saldo = VALOR"
        euros, centimos = get_euros_centimos(saldo_atual)
        moedas_invalidas_message = map(lambda x: re.sub("MOEDA", x, padrao_moeda_invalida), 
                                moedas_invalidas)
        saldo_message = re.sub("VALOR", f"{euros}e{centimos}c", padrao_saldo)
        return 'maq: ' + '; '.join(moedas_invalidas_message) + '; ' + saldo_message

def deal_with_call(operacao, saldo):

    numero_invalido = { "601", "641" }

    precos = {
            "00": 150,
            "2": 25,
            "800": 0,
            "808": 10,
            }

    numero_telemovel = operacao.group(1)
    r1 = re.compile(r"^(?P<comeco>00|2|800|808|641|601)\d+$")

    resultado = r1.match(numero_telemovel)
    if not resultado:
        raise InvalidNumber("Número de telemóvel inválido")

    comeco = resultado.group("comeco")

    if comeco in numero_invalido:
        raise InvalidNumber("Esse número não é permitido neste telefone. Queira discar novo número!")

    preco = precos[comeco]
    if saldo < preco:
        raise SaldoInsuficiente("Saldo insuficiente")

    return preco

def main():
    ativo = False
    terminar = False

    while not ativo:
        operacao = input()
        if re.match(levantar_regex, operacao):
            ativo = True
        else:
            print("Necessita levantar o auscultador primeiro")

    saldo_atual = 0
    print("maq: Introduza moedas.")
    while not terminar:
        operacao = input()
        operacao_levantar = levantar_regex.match(operacao)
        operacao_moedas = moedas_regex.match(operacao)
        operacao_telefonar = telefone_regex.match(operacao)
        operacao_abortar = abortar_regex.match(operacao)
        operacao_pousar = pousar_regex.match(operacao)
        if operacao_moedas:
            resultado = deal_with_moedas(operacao_moedas)
            saldo_atual += resultado[0]
            print(get_message_moedas(saldo_atual, resultado[1]))
        elif operacao_telefonar:
            try:
                preco = deal_with_call(operacao_telefonar, saldo_atual)
                saldo_atual -= preco
                euros, centimos = get_euros_centimos(saldo_atual)
                print("map:", f"saldo = {euros}e{centimos}c")
            except InvalidNumber as e:
                print("maq:", e)
            except SaldoInsuficiente as e:
                print("maq:", e)
        elif operacao_abortar:
            print(f"maq: operação abortada; troco={get_quantidade_moedas(saldo_atual)}; Volte sempre!")
            terminar = True
        elif operacao_pousar:
            print(f"maq: troco={get_quantidade_moedas(saldo_atual)}; Volte sempre!")
            terminar = True
        elif operacao_levantar:
            print("Já está levantado")

if __name__ == "__main__":
    main()
