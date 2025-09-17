import os

def save_output(filename: str, content: str):
    """Сохраняет вывод агента в файл"""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    path = os.path.join(os.getcwd(), filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
        print(f"Сохранен вывод в файл: {path}")