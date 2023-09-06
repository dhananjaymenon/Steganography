import base64


def file_to_base64(file_path: str) -> str:
    with open(file_path, 'rb') as file:
        file_data = file.read()
        base64_data = base64.b64encode(file_data)
        base64_string = base64_data.decode('utf-8')
        return base64_string


def base64_to_binary(base64_string: str) -> str:
    decoded_data = base64.b64decode(base64_string)
    return decoded_data


def binary_to_bs(binary_data: bytes) -> str:
    binary_string = ''.join(format(byte, '08b') for byte in binary_data)
    return binary_string


"""------------"""


def bs_to_binary(binary_string: str) -> bytes:
    binary_data = bytes(int(binary_string[i:i + 8], 2) for i in range(0, len(binary_string), 8))
    return binary_data


def binary_to_base64(binary_data: bytes) -> str:
    encoded_data = base64.b64encode(binary_data)
    base64_string = encoded_data.decode('utf-8')
    return base64_string


def base64_to_file(base64_string: str, output_path: str):
    decoded_data = base64.b64decode(base64_string)
    with open(output_path, 'wb') as file:
        file.write(decoded_data)


"""------------"""


def file_to_binary(file_path: str) -> str:
    base64_string = file_to_base64(file_path)
    binary_data = base64_to_binary(base64_string)
    binary_string = binary_to_bs(binary_data)
    return binary_string


def binary_to_file(binary_string: str, output_file: str, ext: str):
    binary_data = bs_to_binary(binary_string)
    base64_string = binary_to_base64(binary_data)
    base64_to_file(base64_string, output_file+"."+ext)