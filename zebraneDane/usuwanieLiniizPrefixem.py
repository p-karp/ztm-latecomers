def remove_lines_starting_with(prefix):
    for d in ["29-06", "30-06", "01-07", "02-07", "04-07", "05-07"]:
        with open("dane_" + d + ".csv", 'r', encoding='windows-1250') as file:
            lines = file.readlines()

        with open("./dane_ok/dane_" + d + ".csv", 'w', encoding='windows-1250') as file:
            for line in lines:
                if not line.startswith(prefix):
                    file.write(line)

prefix = 'KS Polonia'

remove_lines_starting_with(prefix)