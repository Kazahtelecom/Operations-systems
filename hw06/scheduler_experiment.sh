#!/bin/bash
# Демонстрация влияния nice на производительность процессов

set -euo pipefail

# Проверка прав root
if [[ $EUID -ne 0 ]]; then
    echo "Ошибка: для использования отрицательного nice нужны права администратора."
    echo "Запустите так: sudo bash $0"
    exit 1
fi

# Массив для хранения PID фоновой нагрузки
LOAD_PIDS=()

# Очистка при завершении
cleanup() {
    echo -e "\n[!] Завершение фоновой нагрузки..."
    if [[ ${#LOAD_PIDS[@]} -gt 0 ]]; then
        kill "${LOAD_PIDS[@]}" 2>/dev/null || true
    fi
}

trap cleanup EXIT

echo "[+] Создание фоновой нагрузки (3 процесса dd)..."
for i in {1..3}; do
    dd if=/dev/urandom of=/dev/null bs=1M 2>/dev/null &
    LOAD_PIDS+=($!)
done

echo "[+] Запуск эксперимента: nice -10 vs nice 10..."
echo "------------------------------------------------"

# Высокий приоритет
{ time nice -n -10 dd if=/dev/urandom of=/dev/null bs=1M count=3000 2>/dev/null; } \
    2> high_priority.time &
PID_HIGH=$!

# Низкий приоритет
{ time nice -n 10 dd if=/dev/urandom of=/dev/null bs=1M count=3000 2>/dev/null; } \
    2> low_priority.time &
PID_LOW=$!

echo "[*] Ждем завершения тестовых процессов..."
echo "    High Priority PID: $PID_HIGH"
echo "    Low Priority PID : $PID_LOW"

# Ждем ТОЛЬКО тестовые процессы
wait "$PID_HIGH" "$PID_LOW"

echo
echo "=== РЕЗУЛЬТАТЫ ЭКСПЕРИМЕНТА ==="
echo "--- nice -10 (High Priority) ---"
cat high_priority.time

echo
echo "--- nice 10 (Low Priority) ---"
cat low_priority.time

# Удаление временных файлов
rm -f high_priority.time low_priority.time
