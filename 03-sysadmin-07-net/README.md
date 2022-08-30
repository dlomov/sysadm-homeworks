# Домашнее задание к занятию "3.7. Компьютерные сети, лекция 2"

1. Проверьте список доступных сетевых интерфейсов на вашем компьютере. Какие команды есть для этого в Linux и в Windows?

Ubuntu
```
ip link show
```
Windows 10
```
ipconfig /all
```
2. Какой протокол используется для распознавания соседа по сетевому интерфейсу? Какой пакет и команды есть в Linux для этого?

- `Протокол LLDP` — открытая альтернатива проприетарному протоколу CDP от Cisco
- Пакет `lldpd` команды:
	- lldpctl — посмотреть соседей
	- lldpcli sh neigh — посмотреть соседей
	- lldpcli sh stat sum — общая статистика по всем интерфейсам
	- lldpcli sh int — информация по интерфейсам, на которых запущен lldpd
3. Какая технология используется для разделения L2 коммутатора на несколько виртуальных сетей? Какой пакет и команды есть в Linux для этого? Приведите пример конфига.
- `VLAN` (Virtual LAN)
- `vlan` — пакет в Ubuntu Linux

Пример конфига:
```
network:
  version: 2
  renderer: networkd
  ethernets:
    ens4:
      optional: yes
      addresses: 
        - 10.0.0.2/24
  vlans:
    vlan1001:
      id: 1001
      link: ens4 
      addresses:
        - 10.0.1.2/24
```
4. Какие типы агрегации интерфейсов есть в Linux? Какие опции есть для балансировки нагрузки? Приведите пример конфига.

В Linux bonding и teaming — технологии агрегации сетевых интерфесов в Linux, bonding пришел на замену teaming. 

```bash
vagrant@vagrant:~$ modinfo bonding | grep mode:
parm:           mode:Mode of operation; 0 for balance-rr, 1 for active-backup, 2 for balance-xor, 3 for broadcast, 4 for 802.3ad, 5 for balance-tlb, 6 for balance-alb (charp)
```
Всего их семь. По типам их можно отнести к двум категориям: только фейловер, или фейловер и балансировку.

- `active-backup, broadcast` — обеспечивают только отказоустойчивость
- `balance-tlb, balance-alb, balance-rr, balance-xor, 802.3ad` — обеспечат отказоустойчивость и балансировку

Можно настроить только с одной стороны, или потребуют настройки хоста и свича:

- `active-backup, balance-tlb, balance-alb` настраиваются на хосте
- `broadcast, balance-rr, balance-xor, 802.3ad` потребуют настройки ещё и коммутатора.

Примеры конфига:

active-backup на отказоустойчивость:
```bash
 network:
   version: 2
   renderer: networkd
   ethernets:
     ens3:
       dhcp4: no 
       optional: true
     ens5: 
       dhcp4: no 
       optional: true
   bonds:
     bond0: 
       dhcp4: yes 
       interfaces:
         - ens3
         - ens5
       parameters:
         mode: active-backup
         primary: ens3
         mii-monitor-interval: 2
```
balance-alb, балансировка
```
   bonds:
     bond0: 
       dhcp4: yes 
       interfaces:
         - ens3
         - ens5
       parameters:
         mode: balance-alb
         mii-monitor-interval: 2
```

5. Сколько IP адресов в сети с маской /29 ? Сколько /29 подсетей можно получить из сети с маской /24. Приведите несколько примеров /29 подсетей внутри сети 10.10.10.0/24.
- В сети с маской /29 `досупных 6` адресов плюс 1 сетевой адрес и 1 броадкаст
- На 32 подсети с маской /29 можно резделить сеть с маской /24
- пример /29 подсетей внутри сети 10.10.10.0/24:
	- 10.10.10.8/29, 10.10.10.16/29, 10.10.10.24/29, 10.10.10.32/29
```bash
vagrant@vagrant:~$ ipcalc 10.10.10.0/29 -b
Address:   10.10.10.0
Netmask:   255.255.255.248 = 29
Wildcard:  0.0.0.7
=>
Network:   10.10.10.0/29
HostMin:   10.10.10.1
HostMax:   10.10.10.6
Broadcast: 10.10.10.7
Hosts/Net: 6                     Class A, Private Internet
```

6. Задача: вас попросили организовать стык между 2-мя организациями. Диапазоны 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 уже заняты. Из какой подсети допустимо взять частные IP адреса? Маску выберите из расчета максимум 40-50 хостов внутри подсети.

- Возьмем из подсети 100.64.0.0
- Маска для диапазонов будет /26, она позволит подключить 62 хоста

```bash
vagrant@vagrant:~$ ipcalc 100.64.0.0/26 -b -s 50
Address:   100.64.0.0
Netmask:   255.255.255.192 = 26
Wildcard:  0.0.0.63
=>
Network:   100.64.0.0/26
HostMin:   100.64.0.1
HostMax:   100.64.0.62
Broadcast: 100.64.0.63
Hosts/Net: 62                    Class A

1. Requested size: 50 hosts
Netmask:   255.255.255.192 = 26 
Network:   100.64.0.0/26
HostMin:   100.64.0.1
HostMax:   100.64.0.62
Broadcast: 100.64.0.63
Hosts/Net: 62                    Class A
Needed size:  64 addresses.
Used network: 100.64.0.0/26
```

7. Как проверить ARP таблицу в Linux, Windows? Как очистить ARP кеш полностью? Как из ARP таблицы удалить только один нужный IP?

- Проверить ARP таблицу в 
	- Linux `ip neigh, arp -n` arp входит в пакет net-tools
	- Windows `arp -a`
- Очистить ARP кеш
	- Linux `ip -s -s neigh flush all`
	- Windows `netsh interface IP delete arpcache`
- Удалить IP 
	- Linux, Windows `arp -d <ip-address>`
```bash
sudo apt install net-tools
vagrant@vagrant:~$ arp
Address      HWtype  HWaddress           Flags Mask     Iface
10.0.2.3     ether   32:24:00:82:35:03   C              eth0 
_gateway     ether   32:24:00:82:35:02   C              eth0
```

 ---
## Задание для самостоятельной отработки (необязательно к выполнению)

 8*. Установите эмулятор EVE-ng.
 
 Инструкция по установке - https://github.com/svmyasnikov/eve-ng

 Выполните задания на lldp, vlan, bonding в эмуляторе EVE-ng. 
 
 ---