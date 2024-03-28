import pickle

def compression(string):  # string is your input text
    dict = {}
    entry = ''
    index = 1
    for i in range(len(string)):
        entry += string[i]
        if entry not in dict:
            lst = [index]
            encoder = [dict[entry[0:len(entry) - 1]][0] if entry[0:len(entry) - 1] in dict else 0, entry[-1]]
            lst.append(encoder)
            dict[entry] = lst
            index += 1
            entry = ''
    ans = ''
    for x in dict:
        ans += f'<{dict[x][1][0]},{dict[x][1][1]}>'

    return dict, ans  # 'dict' is a dictionary of each symbol with its encoded value, 'ans' is a final encoded version of input


# This function is used to convert your inputed string into an usable dictionary object
def parse(string):
    dict = {}
    index = 1
    incorrect = False
    for i in range(len(string)):
        if string[i] == '<':
            encoderIndex = ''
            encoderTail = ''
            comma = False
            i += 1
            while string[i] != '>':
                if string[i] == ',':
                    comma = True
                    i += 1
                    continue
                if comma:
                    encoderTail += string[i]
                    i += 1
                    continue
                encoderIndex += string[i]
                i += 1

            lst = [[int(encoderIndex), encoderTail], '']
            dict[index] = lst
            index += 1

    return dict


def decompression(string):  # Your input string should be in format <'index', 'entry'>,... . Ex: <0,A><0,B><2,C>
    error = False
    ans, entry = '', ''
    try:
        parse(string)
    except BaseException:
        error = True  # 'error' is true if your input string was not in the correct format.
        return error, ans, {}

    dict = parse(string)
    for x in dict:
        value = dict[x]
        entry += dict[value[0][0]][1] if value[0][0] != 0 else ''
        entry += value[0][1]

        value[1] = entry
        ans += entry
        entry = ''

    return error, ans, dict


# driver code
def main():

    with open('input.txt', 'r') as file:
        text = file.read()

    dictWithSymbols, encoded = compression(text)
    print(dictWithSymbols)

    with open('data.txt', 'w') as f:
        f.write(encoded)

    with open('data.bin', 'wb') as f:
        pickle.dump(dictWithSymbols, f)

    with open('data.bin', 'rb') as f:
        dict = pickle.load(f)
    
    ans = ""
    for x in dict:
        ans += f'<{dict[x][1][0]},{dict[x][1][1]}>'

    print (ans)

    error, decoded, dictWithSymbolsDECODED = decompression(encoded)
    print(decoded)


if __name__ == '__main__':
    main()