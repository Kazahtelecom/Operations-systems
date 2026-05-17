Скрипт fs_audit.sh выполняет аудит файловой системы Linux.
Он анализирует переданную директорию и выводит информацию о:

смонтированных файловых системах
количестве файлов, директорий и символических ссылок
крупнейших файлах (с inode)
различии между df и du

Скрипт использует системные утилиты Linux (df, du, find) и демонстрирует работу с inode и файловыми метаданными.

🚀 Использование
./fs_audit.sh <директория>
Пример:
./fs_audit.sh /etc

Если директория не существует, скрипт завершится с ошибкой.

Результать

./fs_audit.sh /etc
=== Смонтированные файловые системы ===
Filesystem     Type     Size  Used Avail Use% Mounted on
none           tmpfs    3.9G  4.0K  3.9G   1% /mnt/wsl
/dev/sdd       ext4    1007G  1.8G  954G   1% /
none           tmpfs    3.9G   76K  3.9G   1% /mnt/wslg
none           tmpfs    3.9G  532K  3.9G   1% /run
none           tmpfs    3.9G     0  3.9G   0% /run/lock
none           tmpfs    3.9G     0  3.9G   0% /run/shm
tmpfs          tmpfs    782M   20K  782M   1% /run/user/1000

=== Статистика: /etc ===
  Файлов:      680
  Директорий:  169
  Симлинков:   530

=== Топ-5 крупнейших файлов в /etc ===
  Inode      Размер Путь
  1174       215Ki        /etc/ssl/certs/ca-certificates.crt
  769        74Ki         /etc/mime.types
  18465      32Ki         /etc/apparmor.d/usr.lib.snapd.snap-confine.real
  39049      18Ki         /etc/ld.so.cache
  54         17Ki         /etc/X11/rgb.txt


