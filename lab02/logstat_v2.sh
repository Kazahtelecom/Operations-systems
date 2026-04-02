#!/bin/bash
set -euo pipefail

validate_args() {
    local dir="$1"
    if [[ ! -d "$dir" ]]; then
        echo "Ошибка: директория '$dir' не найдена" >&2
        return 1
    fi
}

count_file_lines() {
    local file="$1"
    wc -l < "$file"
}

main() {
    local log_dir="${1:-./logs}"

    validate_args "$log_dir"

    echo "=== Статистика логов ==="
    local total=0

    for file in "$log_dir"/*.log; do
        if [[ -f "$file" ]]; then
            local count
            count=$(count_file_lines "$file")
            printf "  %-30s %d строк\n" "$(basename "$file")" "$count"
            total=$((total + count))
        fi
    done

    echo "Итого: $total строк"
}

main "$@"
