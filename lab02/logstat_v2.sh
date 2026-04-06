#!/bin/bash
set -euo pipefail

# Функция 1: Валидация
check_dir() {
    local dir="$1"
    if [[ ! -d "$dir" ]]; then
        echo "Ошибка: '$dir' не директория."
        exit 1
    fi
}

# Функция 2: Анализ
analyze_logs() {
    local dir="$1"
    echo "Анализ файлов в $dir..."
    find "$dir" -maxdepth 1 -name "*.log" -exec wc -l {} +
}

# Основная логика
main() {
    local target_dir="${1:-./logs}"
    check_dir "$target_dir"
    analyze_logs "$target_dir"
}

main "$@"
