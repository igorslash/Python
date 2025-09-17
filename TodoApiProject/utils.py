import os
from datetime import datetime

def save_output(filename, content):
    """Сохраняет вывод задачи в файл"""
    os.makedirs('output', exist_ok=True)
    filepath = os.path.join('output', filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"# Generated at {timestamp}\n\n")
        f.write(content)
    
    print(f"Output saved to: {filepath}")
    return filepath


def read_output(filename):
    """Читает сохраненный вывод"""
    try:
        with open(os.path.join('output', filename), 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return None