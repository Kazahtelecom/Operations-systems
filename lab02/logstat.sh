#!/bin/bash
set -euo pipefail

# Проверка аргумента
LOG_DIR="${1:-./logs}"

if [[ ! -d "$LOG_DIR" ]]; then
    echo "Ошибка: Директория '$LOG_DIR' не найдена."
    exit 1
fi

echo "=== Анализ директории: $LOG_DIR ==="

# Цикл по файлам (то, что просил робот)
for file in "$LOG_DIR"/*.log; do
    if [[ -f "$file" ]]; then
        count=$(wc -l < "$file")
        echo "Файл: $(basename "$file") — Строк: $count"
    fi
done

# Итоговая статистика через find (чтобы shellcheck не ругался на ls)
total_logs=$(find "$LOG_DIR" -maxdepth 1 -name "*.log" | wc -l)
echo "Всего найдено лог-файлов: $total_logs"
