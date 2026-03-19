#!/bin/bash

# Проверяем, передан ли файл лога
LOG_FILE=$1

if [ -z "$LOG_FILE" ]; then
    echo "Использование: ./analyze.sh <путь_к_логу>"
    exit 1
fi

echo "=== Отчет об анализе лога: $LOG_FILE ==="

# 1. Всего запросов
TOTAL=$(wc -l < "$LOG_FILE")
echo "1. Всего запросов: $TOTAL"

# 2. Уникальные IP
UNIQUE=$(awk '{print $1}' "$LOG_FILE" | sort -u | wc -l)
echo "2. Уникальных IP: $UNIQUE"

# 3. Топ-3 метода (GET, POST и т.д.)
echo "3. Топ-3 метода запросов:"
awk '{print $6}' "$LOG_FILE" | tr -d '"' | sort | uniq -c | sort -nr | head -n 3

# 4. Топ-5 активных IP
echo "4. Топ-5 активных IP:"
awk '{print $1}' "$LOG_FILE" | sort | uniq -c | sort -nr | head -n 5


