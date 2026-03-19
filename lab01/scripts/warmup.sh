#!/bin/bash
# warmup.sh — знакомство с пайп-цепочками
# Автор: Kuandykov Zhasulan

LOG="$1"

if [ -z "$LOG" ]; then
    echo "Использование: ./warmup.sh <файл_лога>"
    exit 1
fi

echo "=== КОЛИЧЕСТВО СТРОК ==="
wc -l < "$LOG"

echo ""
echo "=== ПЕРВЫЕ 5 СТРОК ==="
head -n 5 "$LOG"

echo ""
echo "=== ВСЕ УНИКАЛЬНЫЕ IP (КОЛИЧЕСТВО) ==="
awk '{print $1}' "$LOG" | sort | uniq | wc -l

