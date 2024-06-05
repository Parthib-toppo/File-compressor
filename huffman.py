import heapq
from collections import Counter
import pickle

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(data):
    frequency = Counter(data)
    heap = [Node(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0]

def build_codes(node, binary_string='', codes={}):
    if node.char is not None:
        codes[node.char] = binary_string
        return codes

    if node.left:
        build_codes(node.left, binary_string + '0', codes)
    if node.right:
        build_codes(node.right, binary_string + '1', codes)

    return codes

def huffman_encoding(data):
    if not data:
        return b"", {}

    root = build_huffman_tree(data)
    codes = build_codes(root)
    encoded_data = ''.join(codes[char] for char in data)

    return encoded_data, codes

def save_compressed_file(encoded_data, codes, output_file_path):
    with open(output_file_path, 'wb') as file:
        # Save codes using pickle
        pickle.dump(codes, file)
        # Save encoded data as binary
        byte_array = bytearray()
        for i in range(0, len(encoded_data), 8):
            byte = encoded_data[i:i + 8]
            byte_array.append(int(byte, 2))
        file.write(byte_array)

def compress_file(input_file_path, output_file_path):
    with open(input_file_path, 'rb') as file:
        data = file.read()

    encoded_data, codes = huffman_encoding(data)
    save_compressed_file(encoded_data, codes, output_file_path)

    return output_file_path

def load_compressed_file(input_file_path):
    with open(input_file_path, 'rb') as file:
        codes = pickle.load(file)
        encoded_data = file.read()
        encoded_bits = ''.join(format(byte, '08b') for byte in encoded_data)

    return encoded_bits, codes

def huffman_decoding(encoded_data, codes):
    reverse_codes = {v: k for k, v in codes.items()}
    current_code = ""
    decoded_data = []

    for bit in encoded_data:
        current_code += bit
        if current_code in reverse_codes:
            char = reverse_codes[current_code]
            decoded_data.append(char)
            current_code = ""

    return bytes(decoded_data)

def decompress_file(input_file_path, output_file_path):
    encoded_data, codes = load_compressed_file(input_file_path)
    decoded_data = huffman_decoding(encoded_data, codes)

    with open(output_file_path, 'wb') as file:
        file.write(decoded_data)

    return output_file_path
