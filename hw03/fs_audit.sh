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

    local file_count
    local dir_count
    local link_count

    file_count=$(find "$dir" -type f 2>/dev/null | wc -l)
    dir_count=$(find "$dir" -type d 2>/dev/null | wc -l)
    link_count=$(find "$dir" -type l 2>/dev/null | wc -l)

    echo "  Файлов:      $file_count"
    echo "  Директорий:  $dir_count"
    echo "  Симлинков:   $link_count"
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

    if [[ "$df_used" -gt 0 ]]; then
        percent=$((diff * 100 / df_used))
    else
        percent=0
    fi

    echo "  df used:   ${df_used} KB"
    echo "  du used:   ${du_used} KB"
    echo "  Разница:   ${diff} KB (${percent}%)"
    echo ""
}

main() {
    # Проверка аргумента
    if [[ $# -lt 1 ]]; then
        echo "Использование: $0 <директория>"
        exit 1
    fi

    local TARGET_DIR="$1"

    # Проверка, что это директория
    if [[ ! -d "$TARGET_DIR" ]]; then
        echo "Ошибка: '$TARGET_DIR' не является директорией." >&2
        exit 1
    fi

    show_mounted_fs
    show_dir_stats "$TARGET_DIR"
    show_top_files "$TARGET_DIR"
    show_df_vs_du
}

main "$@"
