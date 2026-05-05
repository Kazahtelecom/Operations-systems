import hashlib, itertools, string
import threading, time

TARGET_HASH = "098f6bcd4621d373cade4e832627b4f6"
CHARSET = string.ascii_lowercase
MAX_LEN = 4
found = threading.Event()
result = [None]

def worker(chunk):
    for candidate in chunk:
        if found.is_set():
            return
        if hashlib.md5(candidate.encode()).hexdigest() == TARGET_HASH:
            result[0] = candidate
            found.set()
            return

def generate_candidates():
    candidates = []
    for length in range(1, MAX_LEN + 1):
        for combo in itertools.product(CHARSET, repeat=length):
            candidates.append(''.join(combo))
    return candidates

def brute_force_threaded(num_threads=4):
    start = time.time()
    candidates = generate_candidates()
    chunk_size = len(candidates) // num_threads
    threads = []

    for i in range(num_threads):
        lo = i * chunk_size
        hi = len(candidates) if i == num_threads - 1 else (i + 1) * chunk_size
        t = threading.Thread(target=worker, args=(candidates[lo:hi],))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    elapsed = time.time() - start
    print(f"Найдено: '{result[0]}'")
    print(f"Время (threading, {num_threads} потоков): {elapsed:.2f} сек")

if __name__ == "__main__":
    brute_force_threaded()
