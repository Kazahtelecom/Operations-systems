#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int main() {
    pid_t pid = fork(); //

    if (pid == 0) {
        // Заменяем текущий процесс программой ls
        execlp("date", "date", NULL);
        perror("exec failed");
        exit(1);
    } else if (pid > 0) {
        int status;
        // Родитель ждет, пока ребенок закончит работу
        waitpid(pid, &status, 0); 

        if (WIFEXITED(status)) {
            printf("Child exited with code: %d\n", WEXITSTATUS(status)); //
        }
    }
    return 0;
}
