import hashlib, itertools, string
import multiprocessing, time, os

TARGET_HASH = "098f6bcd4621d373cade4e832627b4f6"
CHARSET = string.ascii_lowercase
MAX_LEN = 4

def worker(chunk):
    pid = os.getpid()
    for candidate in chunk:
        if hashlib.md5(candidate.encode()).hexdigest() == TARGET_HASH:
            print(f"[PID {pid}] Найдено: '{candidate}'")
            return candidate
    return None

def generate_candidates():
    candidates = []
    for length in range(1, MAX_LEN + 1):
        for combo in itertools.product(CHARSET, repeat=length):
            candidates.append(''.join(combo))
    return candidates

def brute_force_parallel(num_workers=None):
    if num_workers is None:
        num_workers = multiprocessing.cpu_count()

    start = time.time()
    candidates = generate_candidates()
    chunk_size = len(candidates) // num_workers
    chunks = []

    for i in range(num_workers):
        lo = i * chunk_size
        hi = len(candidates) if i == num_workers - 1 else (i + 1) * chunk_size
        chunks.append(candidates[lo:hi])

    print(f"Воркеров: {num_workers}, кандидатов: {len(candidates):,}")

    with multiprocessing.Pool(num_workers) as pool:
        results = pool.map(worker, chunks)

    elapsed = time.time() - start
    found = [r for r in results if r is not None]

    if found:
        print(f"Результат: '{found[0]}'")
    print(f"Время (multiprocessing, {num_workers} воркеров): {elapsed:.2f} сек")

if __name__ == "__main__":
    brute_force_parallel()

