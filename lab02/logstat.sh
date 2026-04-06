#!/bin/bash
set -euo pipefail

# 1. Проверка: передан ли один аргумент
if [[ $# -ne 1 ]]; then
    echo "Использование: $0 <путь_к_файлу_лога>"
    exit 1
fi

LOG_FILE="$1"

# 2. Проверка: существует ли файл и является ли он обычным файлом
if [[ ! -f "$LOG_FILE" ]]; then
    echo "Ошибка: Файл '$LOG_FILE' не найден."
    exit 1
fi

echo "=== Анализ лога: $(basename "$LOG_FILE") ==="

# Считаем общее количество строк
LINE_COUNT=$(wc -l < "$LOG_FILE")
echo "Всего записей: $LINE_COUNT"

# Выводим топ-5 самых частых IP (первая колонка в логе)
echo "--- Топ-5 активных IP ---"
awk '{print $1}' "$LOG_FILE" | sort | uniq -c | sort -rn | head -n 5
