#!/bin/bash

# 1. Добавляем Strict Mode
set -euo pipefail

# 2. Оборачиваем логику в функции
validate_args() {
    # Проверка количества аргументов ($#)
    if [[ $# -ne 1 ]]; then
        echo "Ошибка: Использование: $0 <путь_к_логу>"
        exit 1
    fi

    # Проверка существования файла (-f)
    if [[ ! -f "$1" ]]; then
        echo "Ошибка: Файл '$1' не найден!"
        exit 1
    fi
}

top_ips() {
    # Все переменные внутри функций должны быть local
    local log_file="$1"
    echo "=== Топ-5 активных IP ==="
    awk '{print $1}' "$log_file" | sort | uniq -c | sort -rn | head -n 5
}

count_404() {
    local log_file="$1"
    echo ""
    echo "=== Количество 404 ==="
    # Вместо grep " 404 " "$log_file" | wc -l
    grep -c " 404 " "$log_file" || true
}

top_url() {
    local log_file="$1"
    echo ""
    echo "=== Самый популярный URL ==="
    # Новое требование для HW02[cite: 1]
    awk '{print $7}' "$log_file" | sort | uniq -c | sort -rn | head -1
}

main() {
    local log_file="$1"
    
    validate_args "$@"
    top_ips "$log_file"
    count_404 "$log_file"
    top_url "$log_file"
}

# 3. Точка входа в скрипт[cite: 1]
main "$@"
