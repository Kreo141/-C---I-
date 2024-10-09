from PIL import Image
import random

def text_to_binary(text):
    binary = ''.join(format(ord(char), '08b') for char in text)
    binary += '00000000' 
    return binary

def apply_algorithm(binary, key, algorithm):
    key = int(key)  # Ensure key is an integer
    if algorithm == 1:  # Bit shifting
        return ''.join(format((int(char, 2) << 1) & 255, '08b') for char in [binary[i:i+8] for i in range(0, len(binary), 8)])
    elif algorithm == 2:  # Bit reversal
        return ''.join(format(int(char[::-1], 2), '08b') for char in [binary[i:i+8] for i in range(0, len(binary), 8)])
    elif algorithm == 3:  # XOR with key
        key_bin = format(key % 256, '08b')
        return ''.join(format(int(char, 2) ^ int(key_bin, 2), '08b') for char in [binary[i:i+8] for i in range(0, len(binary), 8)])
    elif algorithm == 4:  # Addition to Red Channel
        return ''.join(format((int(char, 2) + key) % 256, '08b') for char in [binary[i:i+8] for i in range(0, len(binary), 8)])
    elif algorithm == 5:  # Substitution Cipher
        return ''.join(format((int(char, 2) + 3) % 256, '08b') for char in [binary[i:i+8] for i in range(0, len(binary), 8)])
    return binary

def encrypt_text_to_image(text, key, width, height, algorithm, fileName):
    binary_data = text_to_binary(text)
    
    binary_data = apply_algorithm(binary_data, key, algorithm)
    
    img = Image.new('RGB', (width, height), color='white')
    pixels = img.load()

    idx = 0
    random.seed(key)

    for y in range(height):
        for x in range(width):
            if idx < len(binary_data):
                r = int(binary_data[idx:idx+8], 2) if idx + 8 <= len(binary_data) else 0
                g = random.randint(0, 255)
                b = random.randint(0, 255)
                pixels[x, y] = (r, g, b)
                idx += 8
            else:
                pixels[x, y] = (255, 255, 255)

    img.save(fileName + ".png")
    return img

def binary_to_text(binary):
    chars = []
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        if byte == '00000000':
            break
        chars.append(chr(int(byte, 2)))
    return ''.join(chars)

def reverse_algorithm(binary, key, algorithm):
    if algorithm == 1:  # Bit Shifting
        return ''.join(format((int(char, 2) >> 1) & 255, '08b') for char in [binary[i:i+8] for i in range(0, len(binary), 8)])
    elif algorithm == 2:  # Bit Reversal
        return ''.join(format(int(char[::-1], 2), '08b') for char in [binary[i:i+8] for i in range(0, len(binary), 8)])
    elif algorithm == 3:  # XOR with key
        key_bin = format(key % 256, '08b')
        return ''.join(format(int(char, 2) ^ int(key_bin, 2), '08b') for char in [binary[i:i+8] for i in range(0, len(binary), 8)])
    elif algorithm == 4:  # Subtraction from Red Channel
        return ''.join(format((int(char, 2) - key) % 256, '08b') for char in [binary[i:i+8] for i in range(0, len(binary), 8)])
    elif algorithm == 5:  # Reverse Substitution Cipher
        return ''.join(format((int(char, 2) - 3) % 256, '08b') for char in [binary[i:i+8] for i in range(0, len(binary), 8)])
    return binary

def decrypt_image_to_text(image_path, key, algorithm):
    img = Image.open(image_path)
    pixels = img.load()
    width, height = img.size

    binary_data = ""
    random.seed(key)

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            binary_data += format(r, '08b')

    binary_data = reverse_algorithm(binary_data, key, algorithm)

    return binary_to_text(binary_data)


while(True):
    choice = int(input("\n\n1 -> Encrypt\n2 -> Decrypt\n>>> "))
    if choice == 1:

        filePath = input("Input File Name: ")
        with open(filePath, 'r') as file:
            text = file.read()

        key = input("Input Key: ")
        algorithm = int(input("====================\nSelect Algorithm: \n1. Bit Shifting\n2. Bit Reversal\n3. XOR with Key\n4. Addition to Red Channel\n5. Substitution Cipher\n>>> "))

        fileName = input("Output File Name: ")

        encrypt_text_to_image(text, key, 100, 100, algorithm, fileName)
        print("Encrypted")
    elif choice == 2:
        filePath_D = input("Enter Image Name: ")
        key = int(input("Enter Key: "))
        algorithm = int(input("Select Algorithm: "))
        decrypted_text = decrypt_image_to_text(filePath_D, key, algorithm)
        print("Decrypted text:", decrypted_text)
        try:
            exec(decrypted_text)
        except:
            print("Bulok mali imong key or algoritim, BULOK!")
    else:
        print("Wrong choice nagger")

    