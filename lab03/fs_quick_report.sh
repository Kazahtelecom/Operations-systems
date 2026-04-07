#!/bin/bash
set -euo pipefail

TARGET_DIR="${1:-/etc}"

if [[ ! -d "$TARGET_DIR" ]]; then
    echo "Ошибка: '$TARGET_DIR' не найдена" >&2
    exit 1
fi

echo "=== ФС отчёт ==="
echo ""

echo "--- Смонтированные ФС ---"
df -Th 2>/dev/null | head -1
df -Th 2>/dev/null | grep -E 'ext4|tmpfs'
echo ""

echo "--- Статистика: $TARGET_DIR ---"
echo "  Файлов:     $(find "$TARGET_DIR" -type f 2>/dev/null | wc -l)"
echo "  Директорий: $(find "$TARGET_DIR" -type d 2>/dev/null | wc -l)"
echo "  Симлинков:   $(find "$TARGET_DIR" -type l 2>/dev/null | wc -l)"
echo ""

echo "--- Топ-3 крупнейших файла ---"
printf "  %-10s %-12s %s\n" "Inode" "Размер" "Путь"
find "$TARGET_DIR" -type f -printf '%i\t%s\t%p\n' 2>/dev/null \
    | sort -t$'\t' -k2 -rn \
    | head -3 \
    | while IFS=$'\t' read -r inode size path; do
        hr_size=$(numfmt --to=iec-i "$size" 2>/dev/null || echo "${size}B")
        printf "  %-10s %-12s %s\n" "$inode" "$hr_size" "$path"
    done

echo ""
echo "=== Готово ==="
