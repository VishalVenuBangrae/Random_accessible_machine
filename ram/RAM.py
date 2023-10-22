import sys


def read_data(fname):
    with open(fname) as f:
        data = f.read().splitlines()
    return data


def remove_comments(data):
    result = []
    for line in data:
        line = line.strip()
        if not line.startswith("#") and line:  # Exclude comments and empty lines
            result.append(line.upper())
    return result


def create_registers(data):
    registers = {}
    for line in data:
        xs = line.split()
        if len(xs) > 1 and xs[1] == "=":
            registers[xs[0]] = int(xs[2])
        elif len(xs) == 2:
            if xs[1][0] == "R":
                if xs[1] not in registers:
                    registers[xs[1]] = 0
        elif len(xs) == 3:
            if xs[2][0] == 'R':
                if xs[2] not in registers:
                    registers[xs[2]] = 0
    return registers


def create_labels(data):
    labels = {}
    ino = 0
    for line in data:
        xs = line.split()
        if xs:
            if xs[0][-1] == ":":
                labels[xs[0]] = ino
            if len(xs) == 1 or (len(xs) > 1 and xs[1] != "="):
                ino += 1
    return labels


def create_labels_from_code(code):
    labels = {}
    for i, instruction in enumerate(code):
        labeldef = instruction.get('labeldef', None)
        if labeldef:
            labels[labeldef] = i
    return labels


def create_code(data):
    code = []

    for line in data:

        xs = line.split()

        if "INC" in xs:
            if len(xs) == 2:
                code.append({'opcode': "INC", "register1": xs[1]})
            elif len(xs) == 3:
                code.append({'labeldef': xs[0][:-1].upper(), 'opcode': "INC", "register1": xs[2].upper()})
            else:
                code.append({'error': "Invalid INC Instruction"})

        elif "DEC" in xs:
            if len(xs) == 2:
                code.append({'opcode': "DEC", 'register1': xs[1]})
            elif len(xs) == 3:
                code.append({'labeldef': xs[0][:-1].upper(), 'opcode': "DEC", 'register1': xs[2].upper()})
            else:
                code.append({'error': "Invalid DEC Instruction"})

        elif "CLR" in xs:
            if len(xs) == 2:
                code.append({'opcode': "CLR", 'register1': xs[1]})
            elif len(xs) == 3:
                code.append({'labeldef': xs[0][:-1].upper(), 'opcode': "CLR", 'register1': xs[2].upper()})
            else:
                code.append({'error': "Invalid CLR Instruction"})

        elif "MOV" in xs:
            if 2 < len(xs) <= 4:
                if len(xs) == 3:
                    code.append({'opcode': 'MOV', 'register1': xs[1], 'register2': xs[2]})
                else:
                    code.append({'labeldef': xs[0][:-1].upper(), 'opcode': 'MOV', 'register1': xs[2].upper(),
                                 'register2': xs[3].upper()})
            else:
                code.append({'error': "Invalid MOV Instruction"})

        elif "JMP" in xs:
            if 1 < len(xs) <= 4:
                if len(xs) == 2:
                    code.append({'opcode': 'UJMP', 'jmplabel': xs[1].upper()})
                elif len(xs) == 3:
                    if xs[0][0] != "N":
                        code.append({'register1': xs[0].upper(), 'opcode': 'CJMP', 'jmplabel': xs[2].upper()})
                    else:
                        code.append({'labeldef': xs[0][:-1].upper(), 'opcode': 'UJMP', 'jmplabel': xs[2].upper()})
                elif len(xs) == 4:
                    code.append({'labeldef': xs[0][:-1].upper(), 'register1': xs[1], 'opcode': 'CJMP',
                                 'jmplabel': xs[3].upper()})

            else:
                code.append({'error': "Invalid JMP Instruction"})


        elif "CONTINUE" in xs:
            if 1 <= len(xs) <= 2:
                if len(xs) == 1:
                    code.append({'opcode': xs[0].upper()})
                elif len(xs) == 2:
                    code.append({'labeldef': xs[0][:-1].upper(), 'opcode': xs[1].upper()})
                else:
                    code.append({'error': "Invalid CONTINUE Instruction"})
            else:
                code.append({'error': "Invalid Instruction"})
    return code


def run_ram_program(registers, code, labels, data, debug=False):
    pc = 0

    while pc < len(code):
        rec = code[pc]
        if debug:
            print("Executing:", ' '.join(map(str, rec.values())))

        if rec['opcode'] == "INC":
            value = str(rec['register1'])
            registers[value] += 1

        elif rec['opcode'] == "DEC":
            value = rec['register1']
            if registers[value] != 0:
                registers[value] -= 1

        elif rec['opcode'] == "CLR":
            value = rec['register1']
            registers[value] = 0

        elif rec['opcode'] == "MOV":
            register1 = rec['register1']
            register2 = rec['register2']
            registers[register1] = registers[register2]

        elif rec['opcode'] == "UJMP":
            jmplabel = rec['jmplabel']
            pc = labels[jmplabel + ':'] - 1

        elif rec['opcode'] == "CJMP":
            jmplabel = rec['jmplabel']
            register1 = rec['register1']
            if registers[register1] == 0:
                pc = labels[jmplabel + ':'] - 1  # Added colon to match label format

        elif rec['opcode'] == "CONTINUE":
            pass

        pc += 1
    return registers


def main():
    args = sys.argv[1:]
    debugging = False
    filename = ""

    if len(args) == 1:
        filename = args[0]
    elif len(args) == 2 and args[0] == "-d":
        debugging = True
        filename = args[1]
    else:
        print("Usage: python3 RAM.py [-d] filename")
        sys.exit(1)

    data = read_data(filename)
    new_data = remove_comments(data)
    registers = create_registers(new_data)
    labels = create_labels(new_data)
    code = create_code(new_data)

    if debugging:
        print("Input:")
        for register, value in registers.items():
            print(f"{register} ==> {value}")
        result = run_ram_program(registers, code, labels, new_data, debug=True)

    else:
        print("Input:")
        for register, value in registers.items():
            print(f"{register} ==> {value}")
        result = run_ram_program(registers, code, labels, new_data, debug=False)

    print("\nOutput:")
    for register, value in result.items():
        print(f"{register} = {value}")


if __name__ == "__main__":
    main()
