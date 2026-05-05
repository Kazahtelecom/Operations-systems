import hashlib
import itertools
import string
import time

TARGET_HASH = "098f6bcd4621d373cade4e832627b4f6"
CHARSET = string.ascii_lowercase  # a-z, 26 букв
MAX_LEN = 4

def brute_force_sequential():
    start = time.time()
    attempts = 0

    for length in range(1, MAX_LEN + 1):
        for combo in itertools.product(CHARSET, repeat=length):
            candidate = ''.join(combo)
            attempts += 1
            if hashlib.md5(candidate.encode()).hexdigest() == TARGET_HASH:
                elapsed = time.time() - start
                print(f"Найдено: '{candidate}'")
                print(f"Попыток: {attempts:,}")
                print(f"Время: {elapsed:.2f} сек")
                return candidate, elapsed

    elapsed = time.time() - start
    print(f"Не найдено. Попыток: {attempts:,}, Время: {elapsed:.2f} сек")
    return None, elapsed

if __name__ == "__main__":
    brute_force_sequential()
