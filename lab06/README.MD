ps -eo pid,ni,pri,cls,comm --sort=-pcpu | head -15
    PID  NI PRI CLS COMMAND
      1   0  19  TS systemd
    176   0  19  TS snapd
    123   0  19  TS (udev-worker)
    117   0  19  TS (udev-worker)
    207   0  19  TS unattended-upgr
    343   0  19  TS systemd
     97   0  19  TS systemd-udevd
     52  -1  20  TS systemd-journal
    159   0  19  TS systemd-resolve
    179   0  19  TS wsl-pro-service
    190   0  19  TS rsyslogd
    177   0  19  TS systemd-logind
    163   0  19  TS systemd-timesyn
    259   0  19  TS systemd-timedat
kz444gron@jasulan:~$ cat /proc/$$/stat | awk '{print "PID=" $1, "PRI=" $18, "NI=" $19}'
PID=299 PRI=20 NI=0
kz444gron@jasulan:~$ chrt -p $$
pid 299's current scheduling policy: SCHED_OTHER
pid 299's current scheduling priority: 0

nice -n 0  dd if=/dev/urandom of=/dev/null bs=1M count=2000 2>/dev/null &
PID_HIGH=$!
nice -n 19 dd if=/dev/urandom of=/dev/null bs=1M count=2000 2>/dev/null &
PID_LOW=$!

# Сразу же проверяем их состояние, пока они не завершились:
ps -o pid,ni,pri,%cpu,stat,comm -p $PID_HIGH,$PID_LOW
cat /proc/$PID_HIGH/stat | awk '{print "HIGH: PRI=" $18, "NI=" $19}'
cat /proc/$PID_LOW/stat  | awk '{print "LOW:  PRI=" $18, "NI=" $19}'
[1] 540
[2] 541
    PID  NI PRI %CPU STAT COMMAND
    540   0  19  0.0 R    dd
    541  19   0  0.0 RN   dd
HIGH: PRI=20 NI=0
LOW:  PRI=39 NI=19
kz444gron@jasulan:~/os-kaznu-2026/lab06$ dd if=/dev/urandom of=/dev/null bs=1M &
PID_TEST=$!
[3] 547
[1]   Done                    nice -n 0 dd if=/dev/urandom of=/dev/null bs=1M count=2000 2> /dev/null
[2]   Done                    nice -n 19 dd if=/dev/urandom of=/dev/null bs=1M count=2000 2> /dev/null
kz444gron@jasulan:~/os-kaznu-2026/lab06$ ps -o pid,ni,pri,comm -p $PID_TEST
    PID  NI PRI COMMAND
    547   0  19 dd
kz444gron@jasulan:~/os-kaznu-2026/lab06$ renice -n 10 -p $PID_TEST
# Проверьте изменения через ps
547 (process ID) old priority 0, new priority 10
kz444gron@jasulan:~/os-kaznu-2026/lab06$ renice -n 0 -p $PID_TEST
renice: failed to set priority for 547 (process ID): Permission denied
kz444gron@jasulan:~/os-kaznu-2026/lab06$ kill $PID_TEST
kz444gron@jasulan:~/os-kaznu-2026/lab06$ for i in {1..4}; do dd if=/dev/urandom of=/dev/null bs=1M & done
[4] 556
[5] 557
[6] 558
[7] 559
[3]   Terminated              dd if=/dev/urandom of=/dev/null bs=1M
kz444gron@jasulan:~/os-kaznu-2026/lab06$ { time nice -n 0  dd if=/dev/urandom of=/dev/null bs=1M count=500 2>/dev/null ; } 2> time_high.txt &
{ time nice -n 19 dd if=/dev/urandom of=/dev/null bs=1M count=500 2>/dev/null ; } 2> time_low.txt &
wait
[8] 560
[9] 561
echo "=== NICE 0 ===" && grep real time_high.txt
echo "=== NICE 19 ===" && grep real time_low.txt
killall dd
