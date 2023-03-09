import re

class Camp:
    def __init__(self, nome_campo, range_acumulador = (None, None)):
        self.nome_campo = nome_campo
        self.range_acumulador = range_acumulador[0]
        self.acumulador = range_acumulador[1]

    def __str__(self):
        return "Nome do campo: {0}, Range: {1}, Acumulador: {2}".format(self.nome_campo, self.range_acumulador, self.acumulador)

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
        camps[index] = Camp(nome, (parse_range(range_ac), acumulador))
        print(camps[index])

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

    with open(file_name + "_json.txt", "w") as file:
        file.write(str(content))

def main():
    parse_file("content.txt")

if __name__ == "__main__":
    main()
