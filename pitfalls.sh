#!/bin/bash
set -euo pipefail
# ЛОВУШКА 1: Пробелы в именах файлов
echo "--- Pitfall 1: Word Splitting ---"
filename="my file.txt"
rm "$filename"
# bash видит: rm "my file.txt"
# → удаляет один файл

echo "Пробуем удалить БЕЗ кавычек..."
# rm $filename  # РАСКОММЕНТИРУЙ ЭТО, чтобы увидеть ошибку rm: cannot remove 'my': No such file...
echo "Пробуем удалить С кавычками..."
rm "$filename"  # Вот так правильно

# ЛОВУШКА 2: Пробелы вокруг знака "="
echo -e "\n--- Pitfall 2: Spaces in Assignment ---"
echo "$var"  # Это вызовет ошибку 'command not found'
name="Jassulan"    # Правильно: без пробелов
echo "Привет, $name"

# ЛОВУШКА 3: Молчаливое падение
echo -e "\n--- Pitfall 3: Silent Failures ---"
# set -e # РАСКОММЕНТИРУЙ ЭТО, чтобы скрипт остановился на ошибке

ls /папка/которой/нет
echo "Я все равно напечатаюсь, если 'set -e' выключен!"
