#!/bin/bash
set -euo pipefail

show_mounted_fs() {
    echo "=== Смонтированные файловые системы ==="
    df -Th 2>/dev/null | grep -E 'Filesystem|ext4|tmpfs'
    echo ""
}

show_dir_stats() {
    local dir="$1"

    echo "=== Статистика: $dir ==="
    echo "  Файлов:      $(find "$dir" -type f 2>/dev/null | wc -l)"
    echo "  Директорий:  $(find "$dir" -type d 2>/dev/null | wc -l)"
    echo "  Симлинков:   $(find "$dir" -type l 2>/dev/null | wc -l)"
    echo ""
}

show_top_files() {
    local dir="$1"

    echo "=== Топ-5 крупнейших файлов в $dir ==="
    printf "  %-10s %-12s %s\n" "Inode" "Размер" "Путь"

    find "$dir" -type f -printf '%i\t%s\t%p\n' 2>/dev/null \
        | sort -t$'\t' -k2 -rn \
        | head -5 \
        | while IFS=$'\t' read -r inode size path; do
            local hr_size
            hr_size=$(numfmt --to=iec-i "$size" 2>/dev/null || echo "${size}B")
            printf "  %-10s %-12s %s\n" "$inode" "$hr_size" "$path"
        done

    echo ""
}

show_df_vs_du() {
    echo "=== df vs du (/) ==="

    local df_used
    local du_used
    local diff
    local percent

    df_used=$(df --output=used / | tail -1)
    du_used=$(sudo du -sk / 2>/dev/null | awk '{print $1}')

    diff=$((df_used - du_used))
    percent=$((diff * 100 / df_used))

    echo "  df used:   ${df_used} KB"
    echo "  du used:   ${du_used} KB"
    echo "  Разница:   ${diff} KB (${percent}%)"
    echo ""
}

main() {
    if [[ $# -lt 1 ]]; then
        echo "Использование: $0 <directory>"
        exit 1
    fi

    local target="$1"

    if [[ ! -d "$target" ]]; then
        echo "Ошибка: директория '$target' не существует" >&2
        exit 1
    fi

    show_mounted_fs
    show_dir_stats "$target"
    show_top_files "$target"
    show_df_vs_du
}

main "$@"
