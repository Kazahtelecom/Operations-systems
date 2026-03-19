#!/bin/bash

# Скрипт: analyze.sh
# Цель: Анализ веб-лога и вывод статистики по запросам и IP
# Автор: Kuandykov Zhasulan

LOG_FILE=$1

# 1. Проверка: передан ли аргумент
if [ -z "$LOG_FILE" ]; then
    echo "Ошибка: Аргумент не передан. Использование: ./analyze.sh <путь_к_логу>"
    exit 1
fi

# 2. Проверка: существует ли файл
if [ ! -f "$LOG_FILE" ]; then
    echo "Ошибка: Файл '$LOG_FILE' не найден!"
    exit 1
fi

echo "=== Отчет об анализе лога: $LOG_FILE ==="

# 3. Всего запросов
TOTAL=$(wc -l < "$LOG_FILE")
echo "1. Всего запросов: $TOTAL"

# 4. Уникальные IP
UNIQUE=$(awk '{print $1}' "$LOG_FILE" | sort -u | wc -l)
echo "2. Уникальных IP: $UNIQUE"

# 5. Топ-3 метода (GET, POST и т.д.)
echo "3. Топ-3 метода запросов:"
awk '{print $6}' "$LOG_FILE" | tr -d '"' | sort | uniq -c | sort -nr | head -n 3

# 6. Топ-5 активных IP
echo "4. Топ-5 активных IP:"
awk '{print $1}' "$LOG_FILE" | sort | uniq -c | sort -nr | head -n 5

echo "======================================="
