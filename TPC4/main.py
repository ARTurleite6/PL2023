import re

class Camp:
    def __init__(self, nome_campo, range_acumulador = (None, None)):
        self.nome_campo = nome_campo
        self.range_acumulador = range_acumulador[0]
        self.acumulador = range_acumulador[1]

    def __str__(self):
        return "Nome do campo: {0}, Range: {1}, Acumulador: {2}".format(self.nome_campo, self.range_acumulador, self.acumulador)


def average(values):
    return sum(values) / len(values)

acumulators = {
    "sum": sum,
    "media": average,
        }

def parse_range(range):
    regex_range = r"\{(\d+)(?:,(\d+))?\}"
    r1 = re.compile(regex_range)

    match = r1.match(range)
    if match is not None:
        groups = match.groups()
        return groups

    return None

def get_pattern(pattern):
    regex_camp = r"(?P<nome_campo>\w+)(?P<range>{[\d+,]+})?(?:::(?P<acumulador>\w+))?"
    r1 = re.compile(regex_camp)
    camps = r1.findall(pattern)

    for (index, camp) in enumerate(camps):
        nome, range_ac, acumulador = camp
        acumulador = acumulador.lower() if acumulador != "" else None
        camps[index] = Camp(nome, (parse_range(range_ac), acumulador))

    return camps

def parse_line(line, pattern, regex):
    camps = regex.findall(line)
    if line[-1] == ',':
        camps.append('')
    cenas = {}
    camps = camps[::2]
    for p in pattern:
        if p.range_acumulador is None:
            cenas[p.nome_campo] = camps.pop(0)
        else:
            cenas[p.nome_campo] = []
            for _ in range(int(p.range_acumulador[0])):
                cenas[p.nome_campo].append(camps.pop(0))
            if len(p.range_acumulador) == 2:
                for _ in range(int(p.range_acumulador[0]), int(p.range_acumulador[1])):
                    if camps[0] != "":
                        cenas[p.nome_campo].append(camps.pop(0))

        if p.acumulador is not None:
            values = map(lambda x: int(x), cenas[p.nome_campo])
            cenas.pop(p.nome_campo)
            cenas[f"{p.nome_campo}_{p.acumulador}"] = acumulators[p.acumulador](values)
    return cenas

def parse_file(file_path):
    content = []

    match = re.match(r"(.*)\..*", file_path)
    file_name = "out_file"
    if match is not None:
        file_name = match.group(1)


    with open(file_path) as file:
        pattern = get_pattern(file.readline().strip())
    
        regex = r"[^,]*"
        r1 = re.compile(regex)
        for line in map(lambda x: x.strip(), file.readlines()):
            content.append(parse_line(line, pattern, r1))

    json_file = "[\n"
    with open(file_name + ".json", "w") as file:
        for (index_cena, cena) in enumerate(content):
            json_file += "\t{\n"
            cena_lista = list(cena.items())
            for (index, (key, value)) in enumerate(cena_lista):
                if index == len(cena_lista) - 1:
                    json_file += f'\t\t"{key}": "{value}"\n'
                else:
                    json_file += f'\t\t"{key}": "{value}",\n'
            if index_cena == len(content) - 1:
                json_file += "\t}\n"
            else:
                json_file += "\t},\n"
        json_file += "]"
        file.write(json_file)

def main():
    parse_file("content.txt")

if __name__ == "__main__":
    main()
