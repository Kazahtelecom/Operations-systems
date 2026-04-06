#!/bin/bash
set -euo pipefail
current_user=$(whoami)
echo "Привет, $current_user! Сегодня $(date +%F)"
