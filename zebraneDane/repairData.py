import re

def remove_lines_starting_with(prefix):
    for d in ["29-06", "30-06", "01-07", "02-07", "04-07", "05-07"]:
        with open("./orginalne/dane_" + d + ".csv", 'r', encoding='windows-1250') as file:
            lines = file.readlines()

        with open("./dane_ok/dane_" + d + ".csv", 'w', encoding='windows-1250') as file:
            for line in lines:
                if not line.startswith(prefix):
                    file.write(line)

def adjust_time_in_file():
    # Funkcja do zamiany godzin
    def adjust_time(line):
        # Wzorzec do znalezienia godzin w formacie 24:MM
        pattern = re.compile(r'24:(\d{2}):00')
        # Funkcja do zamiany 24:MM na 00:MM, z wyjątkiem 24:00
        def replace_time(match):
            minutes = match.group(1)
            if minutes == '00':
                return match.group(0)
            else:
                return f'00:{minutes}:00'
        # Zastosowanie wzorca do linii tekstu
        return pattern.sub(replace_time, line)
    
    for d in ["29-06", "30-06", "01-07", "02-07", "04-07", "05-07"]:
        # Odczyt pliku wejściowego
        with open("./orginalne/rj_" + d + ".csv", 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # Przetwarzanie każdej linii
        with open("./dane_ok/rj_" + d + ".csv", 'w', encoding='utf-8') as file:
            for line in lines:
                adjusted_line = adjust_time(line)
                file.write(adjusted_line)


def main():
    prefix = 'KS Polonia'
    remove_lines_starting_with(prefix)
    adjust_time_in_file()


if __name__ == "__main__":
    main()