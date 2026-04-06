#!/bin/bash

# Скрипт: backup.sh
# Описание: Бэкап с проверкой аргументов и ротацией последних 3 копий
set -euo pipefail

readonly BACKUP_DIR="$HOME/backups"

# --- Валидация ---
validate_args() {
    if [[ $# -ne 1 ]]; then
        echo "Ошибка: Нужно указать 1 аргумент."
        exit 1
    fi

    if [[ ! -d "$1" ]]; then
        echo "Ошибка: '$1' не является директорией."
        exit 1
    fi
}

# --- Создание архива ---
create_backup() {
    local source_dir="$1"
    local timestamp
    timestamp=$(date +%Y-%m-%d_%H-%M-%S)
    local archive_name="backup_${timestamp}.tar.gz"

    mkdir -p "$BACKUP_DIR"
    tar -czf "$BACKUP_DIR/$archive_name" -C "$(dirname "$source_dir")" "$(basename "$source_dir")"
    echo "Создан бэкап: $archive_name"
}

# --- Ротация (Удаление старых) ---
rotate_backups() {
    # Находим файлы, сортируем по времени, удаляем всё кроме последних 3
    # Используем -r в xargs, чтобы не было ошибки, если удалять нечего
    find "$BACKUP_DIR" -maxdepth 1 -name "backup_*.tar.gz" -printf '%T@ %p\n' | \
        sort -n | \
        head -n -3 | \
        cut -d' ' -f2- | \
        xargs -r rm -f --
}

# --- Основная логика ---
main() {
    validate_args "$@"
    create_backup "$1"
    rotate_backups
    
    # Итоговый отчет для автопроверки
    local count
    count=$(find "$BACKUP_DIR" -maxdepth 1 -name "backup_*.tar.gz" | wc -l)
    echo "Осталось архивов: $count"
}

# Запуск с передачей всех аргументов
main "$@"
