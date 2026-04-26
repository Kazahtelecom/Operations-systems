#include <stdio.h>
#include <unistd.h>

int main() {
    pid_t pid = fork();
    if (pid == 0) {
        printf("Child done\n");
        return 0;   /* Child завершается */
    }
    /* Parent: НЕ вызывает wait — спит 60 секунд */
    printf("Parent sleeping (child is zombie)...\n");
    sleep(60);
    return 0;
}
