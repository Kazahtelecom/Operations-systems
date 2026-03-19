#!/bin/bash
# Скрипт: warmup.sh
# Цель: Вывод базовой системной информации (пользователь, дата, хост, аптайм)
# Автор: Kuandykov Zhasulan

echo "--- System Report ---"
echo "User: $(whoami)"
echo "Date: $(date)"
echo "Hostname: $(hostname)"
echo "Uptime: $(uptime -p)"

