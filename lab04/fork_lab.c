#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>

int main() {
    printf("Before fork: PID=%d\n", getpid());
    pid_t pid = fork();
    if (pid == 0) {
        printf("Child:  PID=%d, PPID=%d\n", getpid(), getppid());
        sleep(30); // Добавили для pstree
    } else if (pid > 0) {
        printf("Parent: PID=%d, child PID=%d\n", getpid(), pid);
        sleep(30);
    }
    return 0;
}
