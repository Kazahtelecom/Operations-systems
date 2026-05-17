#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>

int main() {
    printf("Before fork: PID=%d\n", getpid());

    pid_t pid = fork();

    if (pid == 0) {
        printf("Child:  PID=%d, PPID=%d\n", getpid(), getppid());
    } else if (pid > 0) {
        printf("Parent: PID=%d, child PID=%d\n", getpid(), pid);
    } else {
        perror("fork failed");
        return 1;
    }
    return 0;
}
