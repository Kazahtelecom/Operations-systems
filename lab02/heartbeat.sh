#!/bin/bash

# Lab 02: Скрипт Heartbeat для мониторинга системы
set -euo pipefail

# Файл лога в текущей директории
LOG_FILE="heartbeat.log"

# Проверка: если файла нет, создаем заголовок
if [[ ! -f "$LOG_FILE" ]]; then
    echo "Datetime | Uptime | Load Average" > "$LOG_FILE"
fi

# Получаем данные
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")
UPTIME_DATA=$(uptime -p)
LOAD_AVG=$(uptime | awk -F'load average:' '{ print $2 }' | xargs)

# Записываем в лог
echo "$TIMESTAMP | $UPTIME_DATA | $LOAD_AVG" >> "$LOG_FILE"

echo "Статус системы записан в $LOG_FILE"
