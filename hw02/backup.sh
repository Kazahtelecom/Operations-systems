#!/bin/bash

# ==============================================================================
# Скрипт: backup.sh
# Описание: Резервное копирование директории с ротацией (хранение 3-х последних)
# Автор: Куандыков Жасулан
# ==============================================================================

# Strict mode: прерывать при ошибках, пустых переменных и ошибках в конвейерах
set -euo pipefail

# Константы
readonly BACKUP_DIR="$HOME/backups"
readonly SOURCE_DIR="${1:-}"

# --- Функция валидации аргументов ---
validate_args() {
    if [[ $# -ne 1 ]]; then
        echo "Использование: $0 <source_directory>"
        exit 1
    fi

    if [[ ! -d "$SOURCE_DIR" ]]; then
        echo "Ошибка: Директория '$SOURCE_DIR' не найдена."
        exit 1
    fi

    # Создаем папку для бэкапов, если её нет
    mkdir -p "$BACKUP_DIR"
}

# --- Функция создания архива ---
create_backup() {
    local timestamp
    timestamp=$(date +%Y-%m-%d_%H-%M-%S)
    local archive_name="backup_${timestamp}.tar.gz"
    local archive_path="$BACKUP_DIR/$archive_name"

    # Архивируем. -C переходит в родительскую папку, чтобы в архиве не было лишних путей
    tar -czf "$archive_path" -C "$(dirname "$SOURCE_DIR")" "$(basename "$SOURCE_DIR")"

    echo "Архив: $archive_name"
    echo "Размер: $(du -sh "$archive_path" | cut -f1)"
    echo "Сохранено в: $BACKUP_DIR/"
}

# --- Функция ротации (удаление старых копий) ---
rotate_backups() {
    # find ищет файлы, выводит время изменения (%T@) и путь (%p), сортирует и удаляет лишние
    # head -n -3 выбирает всё, КРОМЕ последних трех
    find "$BACKUP_DIR" -maxdepth 1 -name "backup_*.tar.gz" -printf '%T@ %p\n' | \
        sort -n | \
        head -n -3 | \
        cut -d' ' -f2- | \
        xargs -r rm -f --
}

# --- Функция финального отчета ---
print_report() {
    # Используем массив для безопасного подсчета количества файлов (SC2012-friendly)
    local files
    files=("$BACKUP_DIR"/backup_*.tar.gz)
    local count=0

    # Если файлы существуют, считаем размер массива
    if [[ -e "${files[0]}" ]]; then
        count=${#files[@]}
    fi

    echo "Архивов после ротации: $count"
}

main() {
    echo "=== Резервное копирование ==="
    validate_args "$@"
    echo "Источник: $SOURCE_DIR"
    
    create_backup
    rotate_backups
    print_report
    
    echo "=== Готово ==="
}

main "$@"
