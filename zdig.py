import zlib

def compress_string(data: str, compression_level: int = 6) -> bytes:
    # Преобразуем строку в байты
    data_bytes = data.encode('utf-8')
    # Сжимаем данные
    compressed_data = zlib.compress(data_bytes, level=compression_level)
    return compressed_data

def decompress_string(compressed_data: bytes) -> str:
    # Распаковываем данные
    decompressed_data = zlib.decompress(compressed_data)
    # Преобразуем байты обратно в строку
    return decompressed_data.decode('utf-8')

# использование
original_data = "сжатие данных! " * 100
compressed = compress_string(original_data)
decompressed = decompress_string(compressed)

print(f"Исходный размер: {len(original_data)} байт")
print(f"Сжатый размер: {len(compressed)} байт")
print(f"Данные совпадают после распаковки: {original_data == decompressed}")


#сжатие файла
def compress_file(input_path: str, output_path: str):
    with open(input_path, 'rb') as f_in:
        data = f_in.read()
    compressed_data = zlib.compress(data)
    with open(output_path, 'wb') as f_out:
        f_out.write(compressed_data)

def decompress_file(input_path: str, output_path: str):
    with open(input_path, 'rb') as f_in:
        compressed_data = f_in.read()
    decompressed_data = zlib.decompress(compressed_data)
    with open(output_path, 'wb') as f_out:
        f_out.write(decompressed_data)

#вывод
compress_file("large_data.txt", "compressed.zlib")
decompress_file("compressed.zlib", "decompressed.txt")


#обработка ошибок
def safe_decompress(data: bytes):
    try:
        return zlib.decompress(data)
    except zlib.error as e:
        print(f"Ошибка распаковки: {e}")
        return None

# Пример с битыми данными
corrupted_data = b"invalid_compressed_data"
result = safe_decompress(corrupted_data)  # Выведет ошибку
