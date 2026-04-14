import time
import random
import string
import re
from typing import List

# Импорт нашей библиотеки
import fast_text_proc

def generate_large_text(size_mb: int = 10) -> str:
    """Генерирует случайный текст заданного размера."""
    words = ["hello", "world", "rust", "python", "benchmark", "data", "science", "email@test.com", "foo", "bar"]
    text_parts = []
    current_size = 0
    target_size = size_mb * 1024 * 1024
    
    while current_size < target_size:
        sentence = " ".join(random.choices(words, k=10)) + ". "
        text_parts.append(sentence)
        current_size += len(sentence)
        
    return "".join(text_parts)

def py_tokenize(text: str) -> List[str]:
    """Аналог fast_tokenize на чистом Python."""
    return [w.strip(".,!?;:\"'").lower() for w in text.split() if w.strip(".,!?;:\"'")]

def py_clean(text: str) -> str:
    """Аналог clean_text на чистом Python."""
    # Удаление пунктуации
    translator = str.maketrans('', '', string.punctuation)
    no_punct = text.translate(translator)
    # Lower case
    lower = no_punct.lower()
    # Удаление лишних пробелов
    return " ".join(lower.split())

def py_count_words(text: str) -> int:
    return len(text.split())

def py_extract_emails(text: str) -> List[str]:
    return re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)

def benchmark(func_name, rust_func, py_func, data, iterations=5):
    """Замеряет время и выводит результат."""
    
    # Warmup
    rust_func(data)
    py_func(data)

# Rust timing
    start = time.perf_counter()
    for _ in range(iterations):
        rust_func(data)
    rust_time = (time.perf_counter() - start) / iterations
    
    # Python timing
    start = time.perf_counter()
    for _ in range(iterations):
        py_func(data)
    py_time = (time.perf_counter() - start) / iterations
    
    speedup = py_time / rust_time if rust_time > 0 else float('inf')
    
    print(f"{func_name:<20} | Rust: {rust_time:.4f}s | Py: {py_time:.4f}s | Speedup: {speedup:.2f}x")

if __name__ == "__main__":
    print("Generating 50MB text...")
    large_text = generate_large_text(50)
    print(f"Text size: {len(large_text) / (1024*1024):.2f} MB")
    print("-" * 70)
    print(f"{'Function':<20} | {'Rust Time':<12} | {'Py Time':<12} | {'Speedup'}")
    print("-" * 70)

    benchmark("Tokenize", fast_text_proc.fast_tokenize, py_tokenize, large_text)
    benchmark("Clean Text", fast_text_proc.clean_text, py_clean, large_text)
    benchmark("Count Words", fast_text_proc.count_words, py_count_words, large_text)
    benchmark("Extract Emails", fast_text_proc.extract_emails, py_extract_emails, large_text)
 
 # Benchmark Batch Processing (Parallel vs Sequential Python)
    print("\n--- Batch Processing (Parallelism) ---")
    batch_data = [large_text[:100000] for _ in range(100)] # 100 chunks
    
    start = time.perf_counter()
    fast_text_proc.batch_tokenize(batch_data)
    rust_batch_time = time.perf_counter() - start
    
    start = time.perf_counter()
    [py_tokenize(t) for t in batch_data]
    py_batch_time = time.perf_counter() - start
    
    print(f"Batch Tokenize     | Rust: {rust_batch_time:.4f}s | Py: {py_batch_time:.4f}s | Speedup: {py_batch_time/rust_batch_time:.2f}x")
