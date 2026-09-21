def line_number(input_filename: str, output_filename: str) -> None:
    try:
        input_file = open(input_filename, "r", encoding="utf-8")
        output_file = open(output_filename, "w", encoding="utf-8")

        number = 1

        for line in input_file:
            line = line.rstrip("\n")
            output_file.write("{}. {}\n".format(number, line))
            number += 1

        input_file.close()
        output_file.close()

    except OSError as error:
        print("There was an error reading or writing the file.")
        print(error)
        raise


def parse_functions(filename: str) -> tuple:
    try:
        input_file = open(filename, "r", encoding="utf-8")
        lines = input_file.readlines()
        input_file.close()

        functions = []

        for index in range(len(lines)):
            line = lines[index]

            if line.startswith("def "):
                function_line = index + 1

                definition = line.rstrip("\n")

                if "#" in definition:
                    definition = definition[:definition.find("#")].rstrip()

                open_parenthesis = definition.find("(")
                close_parenthesis = definition.rfind(")")

                function_name = definition[4:open_parenthesis]
                arguments = definition[
                    open_parenthesis + 1:close_parenthesis
                ]

                function_code = definition + "\n"
                next_line = index + 1

                while next_line < len(lines):
                    current_line = lines[next_line]
                    stripped_line = current_line.strip()

                    if stripped_line == "":
                        next_line += 1
                        continue

                    if stripped_line.startswith("#"):
                        next_line += 1
                        continue

                    if current_line == current_line.lstrip():
                        break

                    current_line = current_line.rstrip("\n")

                    if "#" in current_line:
                        current_line = current_line[
                            :current_line.find("#")
                        ].rstrip()

                    if current_line.strip() != "":
                        function_code += current_line + "\n"

                    next_line += 1

                functions.append(
                    (
                        function_line,
                        function_name,
                        arguments,
                        function_code
                    )
                )

        functions.sort(key=lambda item: item[1])

        return tuple(functions)

    except OSError as error:
        print("There was an error reading the file.")
        print(error)
        raise


def main():
    filename = "p1_Stojanovic_Veljko.py"
    output_filename = "p1_Stojanovic_Veljko.py.txt"

    line_number(filename, output_filename)

    result = parse_functions(filename)
    print(result)


main()