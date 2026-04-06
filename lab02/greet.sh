#!/bin/bash
set -euo pipefail

USER_NAME=$(whoami)
CURRENT_DATE=$(date +%Y-%m-%d)
KERNEL=$(uname -r)

echo "Привет, $USER_NAME!"
echo "Дата: $CURRENT_DATE"
echo "Ядро: $KERNEL"
echo "Текущая директория: $PWD"
