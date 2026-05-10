import hashlib
import itertools
import string
import multiprocessing
import time
import os
import sys

# Глобальные настройки
CHARSET = string.ascii_lowercase
MAX_LEN = 5

def worker(args):
    """
    Проверяет список кандидатов на соответствие целевому хешу.
    args: кортеж (chunk, target_hash)
    """
    chunk, target_hash = args

    pid = os.getpid()
    for candidate in chunk:
        if hashlib.md5(candidate.encode()).hexdigest() == target_hash:
            return candidate, pid
    return None

def generate_candidates():
    """Генерирует полный список всех возможных комбинаций до MAX_LEN."""
    candidates = []
    for length in range(1, MAX_LEN + 1):
        for combo in itertools.product(CHARSET, repeat=length):
            candidates.append(''.join(combo))
    return candidates

def brute_force_parallel(target_hash, num_workers=None):
    """Разделяет работу между процессами и запускает пул."""
    if num_workers is None:
        num_workers = multiprocessing.cpu_count()

    start = time.time()
    candidates = generate_candidates()
    
    # Разбиваем список на части для каждого воркера
    chunk_size = len(candidates) // num_workers
    chunks = []
    for i in range(num_workers):
        lo = i * chunk_size
        hi = len(candidates) if i == num_workers - 1 else (i + 1) * chunk_size
        chunks.append((candidates[lo:hi], target_hash))

    print(f"Воркеров: {num_workers}, кандидатов: {len(candidates):,}")

    with multiprocessing.Pool(num_workers) as pool:
        results = pool.map(worker, chunks)

    elapsed = time.time() - start
    found_result = next((r for r in results if r is not None), None)

    if found_result:
        candidate, pid = found_result
        print(f"[PID {pid}] Найдено: '{candidate}'")
    
    print(f"Время выполнения: {elapsed:.2f} сек")

if __name__ == "__main__":
    # Проверка аргументов командной строки (требование HW07)
    if len(sys.argv) < 2:
        print("Использование: python3 brute_force.py <hash>")
        sys.exit(1)
    
    target_hash_input = sys.argv[1]
    brute_force_parallel(target_hash_input)
