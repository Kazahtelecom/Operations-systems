#!/bin/bash
set -euo pipefail

echo "Привет, $(whoami)!"
echo "Дата: $(date +%Y-%m-%d)"
echo "Ядро: $(uname -r)"
echo "Текущая директория: $PWD"
