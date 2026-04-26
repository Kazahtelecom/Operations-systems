fork_lab.c - Это система вызова использует fork "fork()           → создать процесс" 
Создание дочернего процесса и анализ PID/PPID. "Каждый процесс имеет: PID (уникальный номер), PPID (номер родителя), State (R/S/Z/T). Все процессы образуют дерево с корнем init (PID 1)."
launcher_lab.c — Реализация паттерна fork-exec-wait. Запуск системных утилит (ls, date)
zombie_demo.c - просто создаем функцию которое не живой и не мертвый
(статус Z).

mkdir lab05
kz444gron@jasulan:~/os-kaznu-2026$ cd lab05
kz444gron@jasulan:~/os-kaznu-2026/lab05$ nano fork_lab.c
kz444gron@jasulan:~/os-kaznu-2026/lab05$ gcc -Wall -o fork_lab fork_lab.c && ./fork_lab
Before fork: PID=606
Parent: PID=606, child PID=607
Child:  PID=607, PPID=606
kz444gron@jasulan:~/os-kaznu-2026/lab05$ strace -e trace=process ./fork_lab 2>&1
execve("./fork_lab", ["./fork_lab"], 0x7ffd1db9c140 /* 26 vars */) = 0
Before fork: PID=611
clone(child_stack=NULL, flags=CLONE_CHILD_CLEARTID|CLONE_CHILD_SETTID|SIGCHLD, child_tidptr=0x78952943da10) = 612
Child:  PID=612, PPID=611
--- SIGCHLD {si_signo=SIGCHLD, si_code=CLD_EXITED, si_pid=612, si_uid=1000, si_status=0, si_utime=0, si_stime=0} ---
Parent: PID=611, child PID=612
exit_group(0)                           = ?
+++ exited with 0 +++
kz444gron@jasulan:~/os-kaznu-2026/lab05$ pstree -p | grep fork_lab
kz444gron@jasulan:~/os-kaznu-2026/lab05$ nano launcher_lab.c
kz444gron@jasulan:~/os-kaznu-2026/lab05$ cc -Wall -o launcher_lab launcher_lab.c && ./launcher_lab
total 32
drwxrwxrwt  9 root root 4096 Apr 26 14:19 .
drwxr-xr-x 27 root root 4096 Apr 26 14:11 ..
drwxrwxrwx  2 root root   60 Apr 26 14:11 .X11-unix
drwx------  2 root root 4096 Apr 26 14:12 snap-private-tmp
drwx------  3 root root 4096 Apr 26 14:19 systemd-private-0f2f771ab993430e8ca4a8ac12c4a5dc-polkit.service-5pYPZQ
drwx------  3 root root 4096 Apr 26 14:12 systemd-private-0f2f771ab993430e8ca4a8ac12c4a5dc-systemd-logind.service-gUjdQN
drwx------  3 root root 4096 Apr 26 14:12 systemd-private-0f2f771ab993430e8ca4a8ac12c4a5dc-systemd-resolved.service-PSaKNW
drwx------  3 root root 4096 Apr 26 14:12 systemd-private-0f2f771ab993430e8ca4a8ac12c4a5dc-systemd-timesyncd.service-ixq6Ub
drwx------  3 root root 4096 Apr 26 14:12 systemd-private-0f2f771ab993430e8ca4a8ac12c4a5dc-wsl-pro.service-29nhna
Child exited with code: 0
kz444gron@jasulan:~/os-kaznu-2026/lab05$ gcc -Wall -o launcher_lab launcher_lab.c && ./launcher_lab
total 32
drwxrwxrwt  9 root root 4096 Apr 26 14:20 .
drwxr-xr-x 27 root root 4096 Apr 26 14:11 ..
drwxrwxrwx  2 root root   60 Apr 26 14:11 .X11-unix
drwx------  2 root root 4096 Apr 26 14:12 snap-private-tmp
drwx------  3 root root 4096 Apr 26 14:19 systemd-private-0f2f771ab993430e8ca4a8ac12c4a5dc-polkit.service-5pYPZQ
drwx------  3 root root 4096 Apr 26 14:12 systemd-private-0f2f771ab993430e8ca4a8ac12c4a5dc-systemd-logind.service-gUjdQN
drwx------  3 root root 4096 Apr 26 14:12 systemd-private-0f2f771ab993430e8ca4a8ac12c4a5dc-systemd-resolved.service-PSaKNW
drwx------  3 root root 4096 Apr 26 14:12 systemd-private-0f2f771ab993430e8ca4a8ac12c4a5dc-systemd-timesyncd.service-ixq6Ub
drwx------  3 root root 4096 Apr 26 14:12 systemd-private-0f2f771ab993430e8ca4a8ac12c4a5dc-wsl-pro.service-29nhna
Child exited with code: 0
kz444gron@jasulan:~/os-kaznu-2026/lab05$ strace -e trace=process ./launcher_lab 2>&1
execve("./launcher_lab", ["./launcher_lab"], 0x7ffee761c1b0 /* 26 vars */) = 0
clone(child_stack=NULL, flags=CLONE_CHILD_CLEARTID|CLONE_CHILD_SETTID|SIGCHLD, child_tidptr=0x70fa6302ba10) = 1007
wait4(1007, total 32
drwxrwxrwt  9 root root 4096 Apr 26 14:20 .
drwxr-xr-x 27 root root 4096 Apr 26 14:11 ..
drwxrwxrwx  2 root root   60 Apr 26 14:11 .X11-unix
drwx------  2 root root 4096 Apr 26 14:12 snap-private-tmp
drwx------  3 root root 4096 Apr 26 14:19 systemd-private-0f2f771ab993430e8ca4a8ac12c4a5dc-polkit.service-5pYPZQ
drwx------  3 root root 4096 Apr 26 14:12 systemd-private-0f2f771ab993430e8ca4a8ac12c4a5dc-systemd-logind.service-gUjdQN
drwx------  3 root root 4096 Apr 26 14:12 systemd-private-0f2f771ab993430e8ca4a8ac12c4a5dc-systemd-resolved.service-PSaKNW
drwx------  3 root root 4096 Apr 26 14:12 systemd-private-0f2f771ab993430e8ca4a8ac12c4a5dc-systemd-timesyncd.service-ixq6Ub
drwx------  3 root root 4096 Apr 26 14:12 systemd-private-0f2f771ab993430e8ca4a8ac12c4a5dc-wsl-pro.service-29nhna
[{WIFEXITED(s) && WEXITSTATUS(s) == 0}], 0, NULL) = 1007
--- SIGCHLD {si_signo=SIGCHLD, si_code=CLD_EXITED, si_pid=1007, si_uid=1000, si_status=0, si_utime=0, si_stime=0} ---
Child exited with code: 0
exit_group(0)                           = ?
+++ exited with 0 +++
kz444gron@jasulan:~/os-kaznu-2026/lab05$ nano fork_lab.c
kz444gron@jasulan:~/os-kaznu-2026/lab05$ gcc -Wall -o fork_lab fork_lab.c && ./fork_lab
Parent: PID=1014, child PID=1015
Child:  PID=1015, PPID=1014

kz444gron@jasulan:~/os-kaznu-2026/lab05$
kz444gron@jasulan:~/os-kaznu-2026/lab05$ strace -e trace=process ./fork_lab 2>&1
execve("./fork_lab", ["./fork_lab"], 0x7ffea2c89440 /* 26 vars */) = 0
clone(child_stack=NULL, flags=CLONE_CHILD_CLEARTID|CLONE_CHILD_SETTID|SIGCHLD, child_tidptr=0x7d119ae82a10) = 1020
Child:  PID=1020, PPID=1019
Parent: PID=1019, child PID=1020

--- SIGCHLD {si_signo=SIGCHLD, si_code=CLD_EXITED, si_pid=1020, si_uid=1000, si_status=0, si_utime=0, si_stime=0} ---
exit_group(0)                           = ?
+++ exited with 0 +++
kz444gron@jasulan:~/os-kaznu-2026/lab05$
kz444gron@jasulan:~/os-kaznu-2026/lab05$ pstree -p | grep fork_lab
kz444gron@jasulan:~/os-kaznu-2026/lab05$ nano launcher_lab.c
kz444gron@jasulan:~/os-kaznu-2026/lab05$ cc -Wall -o launcher_lab launcher_lab.c && ./launcher_lab
Sun Apr 26 14:24:03 +05 2026
Child exited with code: 0
kz444gron@jasulan:~/os-kaznu-2026/lab05$ gcc -Wall -o fork_lab fork_lab.c && ./fork_lab
Parent: PID=1038, child PID=1039
Child:  PID=1039, PPID=1038

kz444gron@jasulan:~/os-kaznu-2026/lab05$
kz444gron@jasulan:~/os-kaznu-2026/lab05$ nano zombie_demo.c
kz444gron@jasulan:~/os-kaznu-2026/lab05$ gcc -Wall -o zombie_demo zombie_demo.c && ./zombie_demo &
[1] 1084
kz444gron@jasulan:~/os-kaznu-2026/lab05$ Parent sleeping (child is zombie)...
Child done
ps aux | grep Z
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
kz444gr+    1091  0.0  0.0      0     0 pts/0    Z    14:39   0:00 [zombie_demo] <defunct>
kz444gr+    1093  0.0  0.0   4088  2048 pts/0    S+   14:39   0:00 grep --color=auto Z
kz444gron@jasulan:~/os-kaznu-2026/lab05$

