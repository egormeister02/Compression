import pickle
from bitarray import bitarray

class HuffmanNode:
    def __init__(self, word, freq):
        self.word = word
        self.freq = freq
        self.left = None
        self.right = None

class HuffmanData:
    def __init__(self, huffman_tree, compressed_text, padding):
        self.huffman_tree = huffman_tree
        self.compressed_text = compressed_text
        self.padding = padding

def load_huffman_tree(file):
    return pickle.load(file)

def huffman_decode(compressed_text, huffman_tree):
    decoded_text = ""
    current_node = huffman_tree
    for bit in compressed_text:
        if bit == 0:
            current_node = current_node.left
        else:
            current_node = current_node.right
        if current_node.word is not None:
            decoded_text += current_node.word
            current_node = huffman_tree
    return decoded_text

def decompress_text(compressed_text, huffman_tree, padding):
    compressed_text = compressed_text[:-padding]
    decoded_text = huffman_decode(compressed_text, huffman_tree)
    return decoded_text

def huffman_decompress(input_file, output_file):
    with open(input_file, 'rb') as file:
        huffman_data = pickle.load(file)
    huffman_tree = huffman_data.huffman_tree
    compressed_text = huffman_data.compressed_text
    padding = int(huffman_data.padding, 2)
    decoded_text = decompress_text(compressed_text, huffman_tree, padding)
    with open(output_file, 'w') as file:
        file.write(decoded_text)

# Пример использования
if __name__ == "__main__":
    input_file = 'compressed.bin'  # Укажите путь к файлу, который нужно декодировать
    output_file = 'decoded.txt'  # Укажите путь к файлу, в который будет сохранен декодированный текст
    huffman_decompress(input_file, output_file)