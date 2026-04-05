# Backup Script Automation
Этот скрипт делает бэкап указанной директории в `~/backups/` и оставляет последние 3 копии.

## Настройка Cron
Для автоматизации раз в час добавлена запись в `crontab -e`:
`0 * * * * /home/kz444gron/os-kaznu-2026/hw02/backup.sh /home/kz444gron/data`
