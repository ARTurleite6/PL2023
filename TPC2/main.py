from sys import stdin


def main():
    activated = True
    sum = 0
    for line in stdin:
        line = line.rstrip().lower()
        if line == "off":
            activated = False
        elif line == "on":
            activated = True
        elif line == "=":
            if activated:
                print(sum)
                sum = 0
        elif line.isdigit():
            if activated:
                sum += int(line)



if __name__ == "__main__":
    main()
