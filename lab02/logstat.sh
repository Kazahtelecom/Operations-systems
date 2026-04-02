#!/bin/bash
set -euo pipefail

LOG_DIR="${1:-./logs}"

if [[ ! -d "$LOG_DIR" ]]; then
    echo "Ошибка: директория '$LOG_DIR' не найдена"
    exit 1
fi

echo "=== Статистика логов в $LOG_DIR ==="
total=0

for file in "$LOG_DIR"/*.log; do
    if [[ -f "$file" ]]; then
        count=$(wc -l < "$file")
        printf "  %-30s %d строк\n" "$(basename "$file")" "$count"
        total=$((total + count))
    fi
done

echo "==========================="
echo "Итого: $total строк в $(ls -1 "$LOG_DIR"/*.log 2>/dev/null | wc -l) файлах"
