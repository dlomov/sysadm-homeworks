# Домашнее задание к занятию "3.5. Файловые системы"

1. Узнайте о [sparse](https://ru.wikipedia.org/wiki/%D0%A0%D0%B0%D0%B7%D1%80%D0%B5%D0%B6%D1%91%D0%BD%D0%BD%D1%8B%D0%B9_%D1%84%D0%B0%D0%B9%D0%BB) (разряженных) файлах.

	Разряженный файл — файл, в котором последовательности нулевых байтов заменены на информацию об этих последовательностях (список дыр). Дыра — последовательность нулевых байт внутри файла, не записанная на диск. Информация о дырах (смещение от начала файла в байтах и количество байт) хранится в метаданных ФС. Многие приложения и БД хранят информацию в разряженных файлах это файлы которые используют файловую систему более эфективно не позволяя занимать дисковое пространство когда файлы пусты.

1. Могут ли файлы, являющиеся жесткой ссылкой на один объект, иметь разные права доступа и владельца? Почему?
	
	Нет, не могут. Это ссылка на один и тот же inode - в нём хранятся права доступа и имя владельца.

1. Сделайте `vagrant destroy` на имеющийся инстанс Ubuntu. Замените содержимое Vagrantfile следующим:

    ```bash
    Vagrant.configure("2") do |config|
      config.vm.box = "bento/ubuntu-20.04"
      config.vm.provider :virtualbox do |vb|
        lvm_experiments_disk0_path = "/tmp/lvm_experiments_disk0.vmdk"
        lvm_experiments_disk1_path = "/tmp/lvm_experiments_disk1.vmdk"
        vb.customize ['createmedium', '--filename', lvm_experiments_disk0_path, '--size', 2560]
        vb.customize ['createmedium', '--filename', lvm_experiments_disk1_path, '--size', 2560]
        vb.customize ['storageattach', :id, '--storagectl', 'SATA Controller', '--port', 1, '--device', 0, '--type', 'hdd', '--medium', lvm_experiments_disk0_path]
        vb.customize ['storageattach', :id, '--storagectl', 'SATA Controller', '--port', 2, '--device', 0, '--type', 'hdd', '--medium', lvm_experiments_disk1_path]
      end
    end
    ```

    Данная конфигурация создаст новую виртуальную машину с двумя дополнительными неразмеченными дисками по 2.5 Гб.

1. Используя `fdisk`, разбейте первый диск на 2 раздела: 2 Гб, оставшееся пространство.
	```bash
	Command (m for help): F
	Unpartitioned space /dev/sdb: 2.51 GiB, 2683305984 bytes, 5240832 sectors
	Units: sectors of 1 * 512 = 512 bytes
	Sector size (logical/physical): 512 bytes / 512 bytes

	Start     End Sectors  Size
	2048 5242879 5240832  2.5G

	Command (m for help): n
	Partition type
	p   primary (0 primary, 0 extended, 4 free)
	e   extended (container for logical partitions)
	Select (default p): p
	Partition number (1-4, default 1): 1
	First sector (2048-5242879, default 2048):
	Last sector, +/-sectors or +/-size{K,M,G,T,P} (2048-5242879, default 5242879): +2G

	Created a new partition 1 of type 'Linux' and of size 2 GiB.

	Command (m for help): n
	Partition type
	p   primary (1 primary, 0 extended, 3 free)
	e   extended (container for logical partitions)
	Select (default p): p
	Partition number (2-4, default 2): 2
	First sector (4196352-5242879, default 4196352):
	Last sector, +/-sectors or +/-size{K,M,G,T,P} (4196352-5242879, default 5242879):

	Created a new partition 2 of type 'Linux' and of size 511 MiB.


	Command (m for help): w
	The partition table has been altered.
	Calling ioctl() to re-read partition table.
	Syncing disks.
	```

1. Используя `sfdisk`, перенесите данную таблицу разделов на второй диск.

	```bash
	vagrant@vagrant:~$ sudo sfdisk -d /dev/sdb > sdb.dump
	vagrant@vagrant:~$ sudo sfdisk /dev/sdc < sdb.dump
	Checking that no-one is using this disk right now ... OK

	Disk /dev/sdc: 2.51 GiB, 2684354560 bytes, 5242880 sectors
	Disk model: VBOX HARDDISK   
	Units: sectors of 1 * 512 = 512 bytes
	Sector size (logical/physical): 512 bytes / 512 bytes
	I/O size (minimum/optimal): 512 bytes / 512 bytes

	>>> Script header accepted.
	>>> Script header accepted.
	>>> Script header accepted.
	>>> Script header accepted.
	>>> Created a new DOS disklabel with disk identifier 0x480a38f7.
	/dev/sdc1: Created a new partition 1 of type 'Linux' and of size 2 GiB.
	/dev/sdc2: Created a new partition 2 of type 'Linux' and of size 511 MiB.
	/dev/sdc3: Done.

	New situation:
	Disklabel type: dos
	Disk identifier: 0x480a38f7

	Device     Boot   Start     End Sectors  Size Id Type
	/dev/sdc1          2048 4196351 4194304    2G 83 Linux
	/dev/sdc2       4196352 5242879 1046528  511M 83 Linux

	The partition table has been altered.
	Calling ioctl() to re-read partition table.
	Syncing disks.
	vagrant@vagrant:~$ lsblk
	NAME                      MAJ:MIN RM  SIZE RO TYPE 
	sda                         8:0    0   64G  0 disk
	├─sda1                      8:1    0    1M  0 part
	├─sda2                      8:2    0  1.5G  0 part /boot
	└─sda3                      8:3    0 62.5G  0 part
	└─ubuntu--vg-ubuntu--lv 253:0    0 31.3G  0 lvm  /
	sdb                         8:16   0  2.5G  0 disk
	├─sdb1                      8:17   0    2G  0 part
	└─sdb2                      8:18   0  511M  0 part
	sdc                         8:32   0  2.5G  0 disk
	├─sdc1                      8:33   0    2G  0 part
	└─sdc2                      8:34   0  511M  0 part
	```

1. Соберите `mdadm` RAID1 на паре разделов 2 Гб.

	```bash
	sudo mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/sd[bc]1
	```

1. Соберите `mdadm` RAID0 на второй паре маленьких разделов.

	```bash
	sudo mdadm --create /dev/md1 --level=0 --raid-devices=2 /dev/sd[bc]2

	sdb                         8:16   0  2.5G  0 disk
	├─sdb1                      8:17   0    2G  0 part
	│ └─md0                     9:0    0    2G  0 raid1
	└─sdb2                      8:18   0  511M  0 part
	└─md1                     9:1    0 1018M  0 raid0
	sdc                         8:32   0  2.5G  0 disk
	├─sdc1                      8:33   0    2G  0 part
	│ └─md0                     9:0    0    2G  0 raid1
	└─sdc2                      8:34   0  511M  0 part
	└─md1                     9:1    0 1018M  0 raid0
	```
1. Создайте 2 независимых PV на получившихся md-устройствах.

	```bash
	vagrant@vagrant:~$ sudo pvcreate /dev/md0
	Physical volume "/dev/md0" successfully created.
	vagrant@vagrant:~$ sudo pvcreate /dev/md1
	Physical volume "/dev/md1" successfully created.
	vagrant@vagrant:~$ sudo pvs
	PV         VG        Fmt  Attr PSize    PFree   
	/dev/md0   shara     lvm2 a--    <2.00g   <2.00g
	/dev/md1   shara     lvm2 a--  1016.00m 1016.00m
	/dev/sda3  ubuntu-vg lvm2 a--   <62.50g   31.25g
	```

1. Создайте общую volume-group на этих двух PV.

	```bash
	sudo vgcreate shara /dev/md0 /dev/md1
	vagrant@vagrant:~$ sudo vgs
	VG        #PV #LV #SN Attr   VSize   VFree 
	shara       2   0   0 wz--n-  <2.99g <2.99g
	ubuntu-vg   1   1   0 wz--n- <62.50g 31.25g
	```
1. Создайте LV размером 100 Мб, указав его расположение на PV с RAID0.

	```bash
	vagrant@vagrant:~$ sudo lvcreate -L 100m -n shara-lv shara /dev/md1
	Logical volume "shara-lv" created.
	vagrant@vagrant:~$ sudo lvs -o +devices
	LV        VG        Attr       LSize   Devices     
	shara-lv  shara     -wi-a----- 100.00m  /dev/md1(0)
	ubuntu-lv ubuntu-vg -wi-ao---- <31.25g  /dev/sda3(0)
	```

1. Создайте `mkfs.ext4` ФС на получившемся LV.

	```bash
	vagrant@vagrant:~$ sudo mkfs.ext4 /dev/shara/shara-lv
	```
1. Смонтируйте этот раздел в любую директорию, например, `/tmp/new`.

	```bash
	vagrant@vagrant:~$ mkdir /tmp/new
	vagrant@vagrant:~$ sudo mount /dev/shara/shara-lv /tmp/new
	vagrant@vagrant:~$ mount |grep shara
	/dev/mapper/shara-shara--lv on /tmp/new type ext4 (rw,relatime,stripe=256)
	```
1. Поместите туда тестовый файл, например `wget https://mirror.yandex.ru/ubuntu/ls-lR.gz -O /tmp/new/test.gz`.

	```bash
	vagrant@vagrant:/tmp/new$ ls -l
	total 21864
	drwx------ 2 root root    16384 Aug 26 19:39 lost+found
	-rw-r--r-- 1 root root 22369263 Aug 26 19:00 test.gz
	vagrant@vagrant:/tmp/new$ df -h /tmp/new/
	Filesystem                   Size  Used Avail Use% Mounted on
	/dev/mapper/shara-shara--lv   93M   22M   65M  25% /tmp/new
	```

1. Прикрепите вывод `lsblk`.

	```bash
	vagrant@vagrant:/tmp/new$ lsblk
	NAME                      MAJ:MIN RM  SIZE RO TYPE  MOUNTPOINT
	sda                         8:0    0   64G  0 disk
	├─sda1                      8:1    0    1M  0 part
	├─sda2                      8:2    0  1.5G  0 part  /boot
	└─sda3                      8:3    0 62.5G  0 part
	└─ubuntu--vg-ubuntu--lv 253:0    0 31.3G  0 lvm   /
	sdb                         8:16   0  2.5G  0 disk
	├─sdb1                      8:17   0    2G  0 part
	│ └─md0                     9:0    0    2G  0 raid1
	└─sdb2                      8:18   0  511M  0 part
	└─md1                     9:1    0 1018M  0 raid0
		└─shara-shara--lv     253:1    0  100M  0 lvm   /tmp/new
	sdc                         8:32   0  2.5G  0 disk
	├─sdc1                      8:33   0    2G  0 part
	│ └─md0                     9:0    0    2G  0 raid1
	└─sdc2                      8:34   0  511M  0 part
	└─md1                     9:1    0 1018M  0 raid0
		└─shara-shara--lv     253:1    0  100M  0 lvm   /tmp/new
	```

1. Протестируйте целостность файла:

    ```bash
    root@vagrant:~# gzip -t /tmp/new/test.gz
    root@vagrant:~# echo $?
    0
    ```

1. Используя pvmove, переместите содержимое PV с RAID0 на RAID1.

	```bash
	vagrant@vagrant:/tmp/new$ sudo pvmove -n shara-lv /dev/md1 /dev/md0
	/dev/md1: Moved: 24.00%
	/dev/md1: Moved: 100.00%
	lsvlk
	sdb                         8:16   0  2.5G  0 disk
	├─sdb1                      8:17   0    2G  0 part
	│ └─md0                     9:0    0    2G  0 raid1
	│   └─shara-shara--lv     253:1    0  100M  0 lvm   /tmp/new
	└─sdb2                      8:18   0  511M  0 part
	└─md1                     9:1    0 1018M  0 raid0
	sdc                         8:32   0  2.5G  0 disk
	├─sdc1                      8:33   0    2G  0 part
	│ └─md0                     9:0    0    2G  0 raid1
	│   └─shara-shara--lv     253:1    0  100M  0 lvm   /tmp/new
	└─sdc2                      8:34   0  511M  0 part
	└─md1                     9:1    0 1018M  0 raid0
	```
1. Сделайте `--fail` на устройство в вашем RAID1 md.

	```bash
	vagrant@vagrant:/tmp/new$ sudo mdadm --fail /dev/md0 /dev/sdb1
	mdadm: set /dev/sdb1 faulty in /dev/md0
	```
1. Подтвердите выводом `dmesg`, что RAID1 работает в деградированном состоянии.

	```bash
	vagrant@vagrant:/tmp/new$ dmesg | grep md0 | tail -n 2
	[ 4631.657042] md/raid1:md0: Disk failure on sdb1, disabling device.
				md/raid1:md0: Operation continuing on 1 devices.
	```
1. Протестируйте целостность файла, несмотря на "сбойный" диск он должен продолжать быть доступен:

    ```bash
    root@vagrant:~# gzip -t /tmp/new/test.gz
    root@vagrant:~# echo $?
    0
    ```

1. Погасите тестовый хост, `vagrant destroy`.

 
 ---

