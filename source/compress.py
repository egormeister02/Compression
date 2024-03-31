import argparse
import os
import ctypes

# Загрузка библиотеки
if ctypes._os.name == 'nt':  # Если Windows
    my_lib = ctypes.CDLL('libs/libload_dump.dll')
else:  # Если Unix
    my_lib = ctypes.CDLL('libs/libload_dump.so')

class Data_c(ctypes.Structure):
    _fields_ = [("numbers", ctypes.POINTER(ctypes.c_int)),
                ("symbols", ctypes.POINTER(ctypes.c_char)),
                ("size", ctypes.c_int)]

class Data:
    def __init__(self, int_array, byte_array, size):
        self.numbers = int_array
        self.symbols = byte_array
        self.size = size



def load(file_name):
    c_file_name = ctypes.c_char_p(file_name.encode())

    my_lib.my_load.restype = Data_c
    data = my_lib.my_load(c_file_name)

    # Преобразование указателей в массивы
    numbers = ctypes.cast(data.numbers, ctypes.POINTER(ctypes.c_int * data.size)).contents
    symbols = ctypes.cast(data.symbols, ctypes.POINTER(ctypes.c_char * data.size)).contents

    # Копирование данных внутри Python
    dict = Data(list(numbers), list(symbols), data.size)

    # Освобождение выделенной памяти
    libc = ctypes.CDLL("libc.so.6")
    libc.free(data.numbers)
    libc.free(data.symbols)

    return dict



def dump(dict, file_out):
    numbers = []
    symbols = []
    for x in dict:
        numbers.append(dict[x][1][0])
        symbols.append(dict[x][1][1])

    numbers_c = (ctypes.c_int * len(numbers))(*numbers)
    symbols_c = bytes(symbols)
    my_lib.my_dump(file_out.encode(), numbers_c, symbols_c, len(numbers))


def compression(string):  # string is your input text
    dict = {}
    entry = ''
    index = 1
    last_elem_del = 0
    for i in range(len(string)):
        entry += chr(string[i])
        if entry not in dict:
            lst = [index]
            encoder = [dict[entry[0:len(entry) - 1]][0] if entry[0:len(entry) - 1] in dict else 0, ord(entry[-1])]
            lst.append(encoder)
            dict[entry] = lst
            index += 1
            entry = ''
    if entry != '':
        entry += '\0'
        lst = [index]
        encoder = [dict[entry[0:len(entry) - 1]][0], ord(entry[-1])]
        lst.append(encoder)
        dict[entry] = lst
        last_elem_del = 1
        
    dict['@@@@'] = [index + 1, [last_elem_del, 0]]

    return dict  # 'dict' is a dictionary of each symbol with its encoded value, 'ans' is a final encoded version of input


# This function is used to convert your inputed string into an usable dictionary object
def parse(data):
    dict = {}
    index = 1
    incorrect = False
    for i in range(data.size - 1):
        
        lst = [[data.numbers[i], ord(data.symbols[i])], []]
        dict[index] = lst
        index += 1

    return dict, data.numbers[data.size - 1]


def decompression(data):  # Your input string should be in format <'index', 'entry'>,... . Ex: <0,A><0,B><2,C>
    error = False
    ans, entry = [], []
    try:
        parse(data)
    except BaseException:
        error = True  # 'error' is true if your input string was not in the correct format.
        return error, ans, {}

    dict, del_last = parse(data)
    for x in dict:
        value = dict[x]
        if value[0][0] != 0:
            entry.extend(dict[value[0][0]][1])
        entry.append(value[0][1])

        value[1] = entry
        ans.extend(entry)
        entry = []
    if del_last:
        ans = ans[0:-1]
    return error, ans, dict


# driver code
def main(in_file, out_file, decomp = False):
    

    if decomp:
        dict = load(in_file)
        error, decoded, dictWithSymbolsDECODED = decompression(dict)
        with open(out_file, 'wb') as f:
            f.write(bytes(decoded))
    else:
        with open(in_file, 'rb') as file:
            text = file.read()
        dict = compression(text)
        dump(dict, out_file)

    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process input and output files.")
    parser.add_argument("input_file", help="Input file path")
    parser.add_argument("-o", "--output_file", help="Output file path", default=None)
    parser.add_argument("-r", "--reverse", help="Enable reverse mode", action="store_true")
    args = parser.parse_args()

    # Проверка существования входного файла
    if not os.path.exists(args.input_file):
        print(f"Error: Input file '{args.input_file}' does not exist.")
        exit()

    if args.output_file is None:
        # Определение имени файла по умолчанию на основе наличия флага -r
        default_output_file = args.input_file
        if args.reverse:
            default_output_file = '.'.join(default_output_file.split('.')[:-2])
        else:
            default_output_file += '.copress.bin'
        output_file = default_output_file
    else:
        output_file = args.output_file

    main(args.input_file, output_file, args.reverse)