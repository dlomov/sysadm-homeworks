# Домашнее задание к занятию "3.4. Операционные системы, лекция 2"

1. Установка [node_exporter](https://github.com/prometheus/node_exporter/releases) prometheus.
```bash
cd /opt &&\
sudo wget https://github.com/prometheus/node_exporter/releases/download/v1.2.2/node_exporter-1.2.2.linux-amd64.tar.gz &&\
sudo tar xzf node_exporter-1.2.2.linux-amd64.tar.gz &&\
sudo rm -f node_exporter-1.2.2.linux-amd64.tar.gz &&\
sudo touch node_exporter-1.2.2.linux-amd64/node_exporter.env &&\
echo "EXTRA_OPTS=\"--log.level=info\"" | sudo tee node_exporter-1.2.2.linux-amd64/node_exporter.env &&\
sudo mkdir -p /usr/local/lib/systemd/system/ &&\
sudo touch /usr/local/lib/systemd/system/node_exporter.service
```

- Создание [unit-файла](https://www.freedesktop.org/software/systemd/man/systemd.service.html)
```
sudo tee -a /usr/local/lib/systemd/system/node_exporter.service >/dev/null <<EOF
[Unit]
Description="Test! node_exporter service file"

[Service]
EnvironmentFile=/opt/node_exporter-1.2.2.linux-amd64/node_exporter.env
ExecStart=/opt/node_exporter-1.2.2.linux-amd64/node_exporter $EXTRA_OPTS
StandardOutput=file:/var/log/node_exporter.log
StandardError=file:/var/log/node_exporter.log

[Install]
WantedBy=multi-user.target
EOF 
```
- Предусмотрим возможность добавления опций к запускаемому процессу через внешний файл.
Опции можно добавить через файл /opt/node_exporter-1.2.2.linux-amd64/node_exporter.env, в переменной EXTRA_OPTS — `EXTRA_OPTS="--log.level=info"`. Подключение в unit-файл: 
```
[Service]
EnvironmentFile=/opt/node_exporter-1.2.2.linux-amd64/node_exporter.env
```

- Добавим процесс в автозагрузку — systemctl enable. Удостоверимся, что с помощью systemctl процесс корректно стартует, завершается, а после перезагрузки автоматически поднимается.
```bash
sudo systemctl daemon-reload && \
sudo systemctl enable node_exporter.service &&\
sudo systemctl start node_exporter.service &&\
sudo systemctl stop node_exporter.service &&\
sudo systemctl start node_exporter.service &&\
sudo systemctl status node_exporter.service &&\
journalctl -u node_exporter.service
```

```bash
vagrant@vagrant:~$ sudo systemctl daemon-reload && \
> sudo systemctl start node_exporter.service &&\
> sudo systemctl enable node_exporter.service &&\
> sudo systemctl status node_exporter.service &&\
> journalctl -u node_exporter.service
● node_exporter.service - "Test! node_exporter service file"
     Loaded: loaded (/usr/local/lib/systemd/system/node_exporter.service; enabled; vendor preset: enabled)
     Active: active (running) since Thu 2022-08-11 10:53:15 UTC; 1min 3s ago
   Main PID: 1925 (node_exporter)
      Tasks: 4 (limit: 2274)
     Memory: 2.1M
     CGroup: /system.slice/node_exporter.service
             └─1925 /opt/node_exporter-1.2.2.linux-amd64/node_exporter --log.level=info

Aug 11 10:53:15 vagrant systemd[1]: Started "Test! node_exporter service file".
-- Logs begin at Tue 2022-06-07 11:55:04 UTC, end at Thu 2022-08-11 10:54:19 UTC. --
```
2. Ознакомьтесь с опциями node_exporter и выводом `/metrics` по-умолчанию. Приведите несколько опций, которые вы бы выбрали для базового мониторинга хоста по CPU, памяти, диску и сети.

- CPU
```
vagrant@vagrant:~$ curl http://localhost:9100/metrics | grep node_cpu_seconds_

node_cpu_seconds_total{cpu="0",mode="idle"} 21310.78
node_cpu_seconds_total{cpu="0",mode="system"} 5.06
node_cpu_seconds_total{cpu="0",mode="user"} 3.39
node_cpu_seconds_total{cpu="1",mode="idle"} 20737.2
node_cpu_seconds_total{cpu="1",mode="system"} 5.09
node_cpu_seconds_total{cpu="1",mode="user"} 3.02
```
- Память
```
node_memory_MemAvailable_bytes 1.74610432e+09
node_memory_MemFree_bytes 1.074286592e+09
node_memory_SwapCached_bytes 0
node_memory_SwapFree_bytes 2.047864832e+09
node_memory_SwapTotal_bytes 2.047864832e+09
```
- Диск
```bash
node_filesystem_size_bytes	#размер диска
node_filesystem_avail_bytes	#доступный обьем диска
node_filesystem_readonly	#если "1" то диск ушел в режим только чтение
node_disk_io_now			#потребление io
```

3. Установите в свою виртуальную машину [Netdata](https://github.com/netdata/netdata). Воспользуйтесь [готовыми пакетами](https://packagecloud.io/netdata/netdata/install) для установки (`sudo apt install -y netdata`).
```
vagrant@vagrant:~$ sudo apt install -y netdata
```
После успешной установки: 
- в конфигурационном файле `/etc/netdata/netdata.conf` в секции [web] замените значение с localhost на `bind to = 0.0.0.0`,
- добавьте в Vagrantfile проброс порта Netdata на свой локальный компьютер и сделайте `vagrant reload`:

```bash
config.vm.network "forwarded_port", guest: 19999, host: 19999

	C:\VM>vagrant port
The forwarded ports for the machine are listed below. Please note that
these values may differ from values configured in the Vagrantfile if the
provider supports automatic port collision detection and resolution.

    22 (guest) => 2222 (host)
 19999 (guest) => 19999 (host)
```
    После успешной перезагрузки в браузере *на своем ПК* (не в виртуальной машине) вы должны суметь зайти на `localhost:19999`. Ознакомьтесь с метриками, которые по умолчанию собираются Netdata и с комментариями, которые даны к этим метрикам.
- http://localhost:19999/netdata.conf
- http://localhost:19999/

![netdata](https://github.com/dlomov/sysadm-homeworks/blob/master/03-sysadmin-04-os/netdata.PNG)

4. Можно ли по выводу `dmesg` понять, осознает ли ОС, что загружена не на настоящем оборудовании, а на системе виртуализации?
- Да, можно. У меня Vagrant в VirtualBox на Windows 10.
```bash
vagrant@vagrant:~$ dmesg | grep -i 'Hypervisor detected'
[    0.000000] Hypervisor detected: KVM
vagrant@vagrant:~$ dmesg | grep virtualiz
[    0.005737] CPU MTRRs all blank - virtualized system.
[    0.043706] Booting paravirtualized kernel on KVM
[   19.614430] systemd[1]: Detected virtualization oracle
```
5. Как настроен sysctl `fs.nr_open` на системе по-умолчанию?
```bash
vagrant@vagrant:~$ /sbin/sysctl -n fs.nr_open
1048576
```
 - Узнайте, что означает этот параметр. 

Это максимальное количество файловых дескрипторов, которые может открыть процесс, для пользователя задать больше этого числа нельзя (если не менять). Число задается кратное 1024, в данном случае =1024*1024.
Максимальный предел ОС можно посмотреть так :
```bash
vagrant@vagrant:~$ cat /proc/sys/fs/file-max
9223372036854775807
```
- Но такого числа не позволит достичь `ulimit -n`, по-умолчанию оно равно 1024:
```
vagrant@vagrant:~$ ulimit -n
1024
```
6. Запустите любой долгоживущий процесс (не `ls`, который отработает мгновенно, а, например, `sleep 1h`) в отдельном неймспейсе процессов; покажите, что ваш процесс работает под PID 1 через `nsenter`. Для простоты работайте в данном задании под root (`sudo -i`). Под обычным пользователем требуются дополнительные опции (`--map-root-user`) и т.д.

```bash
vagrant@vagrant:~$ sleep 1h
vagrant@vagrant:~$ ps -e | grep sleep
   1499 pts/0    00:00:00 sleep
vagrant@vagrant:~$ sudo nsenter --target 1499 --pid --mount
root@vagrant:/# ps aux -H
root           1  1.2  0.5 101896 11240 ?        Ss   19:35   0:04 /sbin/init
root        1432  0.0  0.4  13788  8988 ?        Ss   19:36   0:00     sshd: vagrant [priv]
vagrant     1484  0.0  0.3  13920  6332 ?        S    19:36   0:00       sshd: vagrant@pts/0
vagrant     1485  0.0  0.2   7356  4324 pts/0    Ss   19:36   0:00         -bash
vagrant     1499  0.0  0.0   5476   520 pts/0    S+   19:38   0:00           sleep 1h
```
7. Найдите информацию о том, что такое `:(){ :|:& };:`. Запустите эту команду в своей виртуальной машине Vagrant с Ubuntu 20.04 (**это важно, поведение в других ОС не проверялось**). Некоторое время все будет "плохо", после чего (минуты) – ОС должна стабилизироваться. Вызов `dmesg` расскажет, какой механизм помог автоматической стабилизации. Как настроен этот механизм по-умолчанию, и как изменить число процессов, которое можно создать в сессии?

- Это [fork-бомба](https://en.wikipedia.org/wiki/Fork_bomb), shell бесконечно создаёт новые экземпляры себя.
- Если установить ulimit -u 50 - число процессов будет ограниченно 50 для пользоователя.

---
