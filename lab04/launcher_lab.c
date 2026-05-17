#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    pid_t pid = fork();
    if (pid == 0) {
        execlp("date", "date", "-la", "/tmp", NULL);
        perror("exec failed");
        exit(1);
    } else if (pid > 0) {
        int status;
        waitpid(pid, &status, 0);
        if (WIFEXITED(status)) {
            printf("Child exited with code: %d\n", WEXITSTATUS(status));
        }
    }
    return 0;
}

