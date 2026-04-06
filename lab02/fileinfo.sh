#!/bin/bash
set -euo pipefail
if [[ $# -ne 1 ]]; then
    echo "Нужен 1 аргумент"
    exit 1
fi
target="$1"
if [[ -e "$target" ]]; then
    echo "Файл: $target"
    echo "Размер: $(du -sh "$target" | cut -f1)"
fi
