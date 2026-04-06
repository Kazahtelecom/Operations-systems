#!/bin/bash

# Скрипт: backup.sh
# Назначение: Резервное копирование с ротацией (оставляем последние 3)
set -euo pipefail

# Константы
readonly BACKUP_DIR="$HOME/backups"
readonly SOURCE_DIR="${1:-}"

# --- Функция валидации ---
validate_args() {
    # Проверка: передан ли аргумент
    if [[ -z "$SOURCE_DIR" ]]; then
        echo "Ошибка: Не указан путь к директории."
        echo "Использование: $0 <source_directory>"
        exit 1
    fi

    # Проверка: является ли аргумент директорией (КРИТИЧНОЕ ТРЕБОВАНИЕ!)
    if [[ ! -d "$SOURCE_DIR" ]]; then
        echo "Ошибка: '$SOURCE_DIR' не является директорией или не существует."
        exit 1
    fi

    mkdir -p "$BACKUP_DIR"
}

# --- Создание бэкапа ---
create_backup() {
    local timestamp
    timestamp=$(date +%Y-%m-%d_%H-%M-%S)
    local archive_name="backup_${timestamp}.tar.gz"
    
    # Архивируем
    tar -czf "$BACKUP_DIR/$archive_name" -C "$(dirname "$SOURCE_DIR")" "$(basename "$SOURCE_DIR")"
    
    echo "=== Создан новый бэкап ==="
    echo "Файл: $archive_name"
    echo "Размер: $(du -sh "$BACKUP_DIR/$archive_name" | cut -f1)"
}

# --- Ротация (КРИТИЧНОЕ ТРЕБОВАНИЕ!) ---
rotate_backups() {
    # 1. Находим все файлы backup_*.tar.gz
    # 2. Сортируем по времени изменения (старые сверху)
    # 3. Выбираем всё, КРОМЕ последних трех (head -n -3)
    # 4. Удаляем
    find "$BACKUP_DIR" -maxdepth 1 -name "backup_*.tar.gz" -printf '%T@ %p\n' | \
        sort -n | \
        head -n -3 | \
        cut -d' ' -f2- | \
        xargs -r rm -f --

    local count
    count=$(find "$BACKUP_DIR" -maxdepth 1 -name "backup_*.tar.gz" | wc -l)
    echo "Архивов после ротации: $count"
}

main() {
    validate_args
    create_backup
    rotate_backups
    echo "=== Готово ==="
}

main
