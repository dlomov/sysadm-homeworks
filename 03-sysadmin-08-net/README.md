# Домашнее задание к занятию "3.8. Компьютерные сети, лекция 3"

1. Подключитесь к публичному маршрутизатору в интернет. Найдите маршрут к вашему публичному IP
```bash
telnet route-views.routeviews.org
Username: rviews
show ip route x.x.x.x/32
show bgp x.x.x.x/32
```
show ip route
```bash
route-views>show ip route xxx.124.xxx.253
Routing entry for xxx.124.xxx.0/24
  Known via "bgp 6447", distance 20, metric 0
  Tag 6939, type external
  Last update from 64.71.137.241 7w0d ago
  Routing Descriptor Blocks:
  * 64.71.137.241, from 64.71.137.241, 7w0d ago
      Route metric is 0, traffic share count is 1
      AS Hops 2
      Route tag 6939
      MPLS label: none
```
show bgp
```bash
route-views>show bgp xxx.124.xxx.253  
BGP routing table entry for 176.124.200.0/24, version 2328105359
Paths: (22 available, best #19, table default)
  Not advertised to any peer
  Refresh Epoch 1
  7660 2516 3257 28917 207651
    203.181.248.168 from 203.181.248.168 (203.181.248.168)
      Origin IGP, localpref 100, valid, external
      Community: 2516:1030 7660:9003
      path 7FE01C6BEA18 RPKI State not found
      rx pathid: 0, tx pathid: 0
  Refresh Epoch 1
  3561 3910 3356 31500 207651 207651
    206.24.210.80 from 206.24.210.80 (206.24.210.80)
      Origin IGP, localpref 100, valid, external
      path 7FE0EA216510 RPKI State not found
```
2. Создайте dummy0 интерфейс в Ubuntu. Добавьте несколько статических маршрутов. Проверьте таблицу маршрутизации.
```bash
vagrant@vagrant:~$ sudo ip link add name dummy0 type dummy
vagrant@vagrant:~$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:a2:6b:fd brd ff:ff:ff:ff:ff:ff
    inet 10.0.2.15/24 brd 10.0.2.255 scope global dynamic eth0
       valid_lft 84556sec preferred_lft 84556sec
    inet6 fe80::a00:27ff:fea2:6bfd/64 scope link
       valid_lft forever preferred_lft forever
4: dummy0: <BROADCAST,NOARP> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether 8a:50:68:23:1a:63 brd ff:ff:ff:ff:ff:ff
```
Добавление постоянного интерфейса и IP-адреса
```bash
vagrant@vagrant:~$ sudo su
cat << "EOF" >> /etc/systemd/network/dummy0.netdev
[NetDev]
Name=dummy0
Kind=dummy 
EOF
cat << "EOF" >> /etc/systemd/network/dummy0.network
[Match]
Name=dummy0

[Network]
Address=192.168.0.100/24
EOF

vagrant@vagrant:~$ sudo systemctl restart systemd-networkd
vagrant@vagrant:~$ ip a
4: dummy0: <BROADCAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc noqueue state UNKNOWN group default qlen 1000
    link/ether 8a:50:68:23:1a:63 brd ff:ff:ff:ff:ff:ff
    inet 192.168.0.100/24 brd 192.168.0.255 scope global dummy0
       valid_lft forever preferred_lft forever
    inet6 fe80::8850:68ff:fe23:1a63/64 scope link
       valid_lft forever preferred_lft forever
```
Добавление маршрута
```bash
ip route add 8.8.8.0/24 via 10.0.2.1
ip route add 8.16.28.0/24 via 192.168.0.100
vagrant@vagrant:~$ ip route
default via 10.0.2.2 dev eth0 proto dhcp src 10.0.2.15 metric 100 
8.8.8.0/24 via 10.0.2.1 dev eth0
8.16.28.0/24 via 192.168.0.100 dev dummy0
10.0.2.0/24 dev eth0 proto kernel scope link src 10.0.2.15
10.0.2.2 dev eth0 proto dhcp scope link src 10.0.2.15 metric 100
192.168.0.0/24 dev dummy0 proto kernel scope link src 192.168.0.100
```
3. Проверьте открытые TCP порты в Ubuntu, какие протоколы и приложения используют эти порты? Приведите несколько примеров.
- port 22 — ssh
- port 53 — DNS
```
vagrant@vagrant:~$ ss -tpan
State          Send-Q        Local Address:Port         Peer Address:Port
LISTEN         4096          127.0.0.53%lo:53           0.0.0.0:*
LISTEN         128           0.0.0.0:22           		0.0.0.0:*
ESTAB          0             10.0.2.15:22          		10.0.2.2:4621
LISTEN         128           [::]:22           			[::]:*
```

4. Проверьте используемые UDP сокеты в Ubuntu, какие протоколы и приложения используют эти порты?
```bash
vagrant@vagrant:~$ ss -upan
State          Send-Q      Local Address:Port       Peer Address:Port
UNCONN         0           127.0.0.53%lo:53         0.0.0.0:*
UNCONN         0           10.0.2.15%eth0:68        0.0.0.0:*
```
- port 68 — DHCP
- port 53 — DNS
5. Используя diagrams.net, создайте L3 диаграмму вашей домашней сети или любой другой сети, с которой вы работали.

![netmapl3:](https://github.com/dlomov/sysadm-homeworks/blob/master/03-sysadmin-08-net/netmap.png)
 ---
## Задание для самостоятельной отработки (необязательно к выполнению)

6*. Установите Nginx, настройте в режиме балансировщика TCP или UDP.

7*. Установите bird2, настройте динамический протокол маршрутизации RIP.

8*. Установите Netbox, создайте несколько IP префиксов, используя curl проверьте работу API.
