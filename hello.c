#include <unistd.h>
#include <stdio.h>

int main() {
    printf("Запускаю /usr/bin/date под именем hello...\n");

    // Параметры execl:
    // 1. "/usr/bin/date" — путь к исполняемому файлу
    // 2. "hello" — это станет значением argv[0] для запущенной программы
    // 3. NULL — признак конца списка аргументов
    execl("/usr/bin/", "hello", NULL);

    // Сюда попадем только если запуск не удался
    perror("exec failed");
    return 1;
}
