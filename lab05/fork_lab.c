#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>

int main() {
    pid_t pid = fork();

    if (pid == 0) {
        printf("Child:  PID=%d, PPID=%d\n", getpid(), getppid());
        sleep(30); // Добавь эту строку, чтобы процесс не завершался сразу
    } else if (pid > 0) {
        printf("Parent: PID=%d, child PID=%d\n", getpid(), pid);
        sleep(30); // Родителю тоже лучше поспать, чтобы дерево сохранилось
    }
    return 0;
}
