#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    pid_t pid = fork();

    if (pid == 0) {
        printf("Child (PID=%d): запускаю ls...\n", getpid());
        execlp("ls", "ls", "-la", "/tmp", NULL);

        /* Сюда попадём ТОЛЬКО если exec не удался */
        perror("exec failed");
        exit(1);
    } else if (pid > 0) {
        printf("Parent (PID=%d): создал child %d\n", getpid(), pid);
    }
    return 0;
}
