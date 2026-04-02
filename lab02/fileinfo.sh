#!/bin/bash
set -euo pipefail

if [[ $# -eq 0 ]]; then
    echo "Использование: $0 <файл>"
    exit 1
fi

FILE="$1"

if [[ ! -f "$FILE" ]]; then
    echo "Ошибка: '$FILE' не найден или не является файлом"
    exit 1
fi

echo "=== Информация о файле ==="
echo "Имя: $FILE"
echo "Строк: $(wc -l < "$FILE")"
echo "Размер: $(du -h "$FILE" | awk '{print $1}')"

if [[ -x "$FILE" ]]; then
    echo "Исполняемый: да"
else
    echo "Исполняемый: нет"
fi
