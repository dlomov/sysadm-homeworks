# Домашнее задание к занятию "3.1. Работа в терминале, лекция 1"
## Ход решения
1. Установите средство виртуализации [Oracle VirtualBox](https://www.virtualbox.org/).
```
Установил версию 6.1 на Windows 10
```
2. Установите средство автоматизации [Hashicorp Vagrant](https://www.vagrantup.com/).
```bash
$ vagrant -v
Vagrant 2.2.19
```
3. В вашем основном окружении подготовьте удобный для дальнейшей работы терминал.

```PowerShell
Печально что Vargran не расботает с включенной WSL, пришлось отключить WSL в PowerShell:
Disable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux 
```
4. С помощью базового файла конфигурации запустите Ubuntu 20.04 в VirtualBox посредством Vagrant.

Создали папку и перешли в нее
```bash
$ mkdir VM && cd VM
```
`Инициализируем` базовый файл
```bash
$ vagrant init
```
Записали конфиг в файл `Vagranfile`
```
$ echo "Vagrant.configure("2") do |config| /
>  config.vm.box = "bento/ubuntu-20.04" /
>  end" >> Vagrantfile
```
Выполнение в этой директории `vagrant up` установит провайдер VirtualBox для Vagrant, скачает необходимый образ и запустит виртуальную машину.
```bash
$ vagrant up
Bringing machine 'default' up with 'virtualbox' provider...
==> default: Box 'bento/ubuntu-20.04' could not be found. Attempting to find and install...
    default: Box Provider: virtualbox
    default: Box Version: >= 0
==> default: Loading metadata for box 'bento/ubuntu-20.04'
    default: URL: https://vagrantcloud.com/bento/ubuntu-20.04
==> default: Adding box 'bento/ubuntu-20.04' (v202206.03.0) for provider: virtualbox
    default: Downloading: https://vagrantcloud.com/bento/boxes/ubuntu-20.04/versions/202206.03.0/providers/virtualbox.box
    default: 
==> default: Successfully added box 'bento/ubuntu-20.04' (v202206.03.0) for 'virtualbox'!
==> default: Importing base box 'bento/ubuntu-20.04'...
==> default: Matching MAC address for NAT networking...
==> default: Checking if box 'bento/ubuntu-20.04' version '202206.03.0' is up to date...
==> default: Setting the name of the VM: VM_default_1655469666005_81291
Vagrant is currently configured to create VirtualBox synced folders with
the `SharedFoldersEnableSymlinksCreate` option enabled. If the Vagrant
guest is not trusted, you may want to disable this option. For more
information on this option, please refer to the VirtualBox manual:

  https://www.virtualbox.org/manual/ch04.html#sharedfolders

This option can be disabled globally with an environment variable:

  VAGRANT_DISABLE_VBOXSYMLINKCREATE=1

or on a per folder basis within the Vagrantfile:

  config.vm.synced_folder '/host/path', '/guest/path', SharedFoldersEnableSymlinksCreate: false
==> default: Clearing any previously set network interfaces...
==> default: Preparing network interfaces based on configuration...
    default: Adapter 1: nat
==> default: Forwarding ports...
    default: 22 (guest) => 2222 (host) (adapter 1)
==> default: Booting VM...
==> default: Waiting for machine to boot. This may take a few minutes...
    default: SSH address: 127.0.0.1:2222
    default: SSH username: vagrant
    default: SSH auth method: private key
Timed out while waiting for the machine to boot. This means that
Vagrant was unable to communicate with the guest machine within
the configured ("config.vm.boot_timeout" value) time period.

If you look above, you should be able to see the error(s) that
Vagrant had when attempting to connect to the machine. These errors
are usually good hints as to what may be wrong.

If you're using a custom box, make sure that networking is properly
working and you're able to connect to the machine. It is a common
problem that networking isn't setup properly in these boxes.
Verify that authentication configurations are also setup properly,
as well.

If the box appears to be booting properly, you may want to increase
the timeout ("config.vm.boot_timeout") value.
```
`vagrant suspend` выключит виртуальную машину с сохранением ее состояния
```bash
$ vagrant suspend
==> default: Saving VM state and suspending execution...
```
При следующем `vagrant up` будут запущены все процессы внутри, которые работали на момент вызова suspend
```bash
$ vagrant up
Bringing machine 'default' up with 'virtualbox' provider...
==> default: Checking if box 'bento/ubuntu-20.04' version '202206.03.0' is up to date...
==> default: Resuming suspended VM...
==> default: Booting VM...
==> default: Waiting for machine to boot. This may take a few minutes...
    default: SSH address: 127.0.0.1:2222
    default: SSH username: vagrant
    default: SSH auth method: private key
    default: 
    default: Vagrant insecure key detected. Vagrant will automatically replace
    default: this with a newly generated keypair for better security.
    default: 
    default: Inserting generated public key within guest...
    default: Removing insecure key from the guest if it's present...
    default: Key inserted! Disconnecting and reconnecting using new SSH key...
==> default: Machine booted and ready!
```
`vagrant halt` выключит виртуальную машину штатным образом.
```bash
$ vagrant halt
==> default: Attempting graceful shutdown of VM...
```
5. Ознакомьтесь с графическим интерфейсом VirtualBox, посмотрите как выглядит виртуальная машина, которую создал для вас Vagrant, какие аппаратные ресурсы ей выделены. Какие ресурсы выделены по-умолчанию?

![Аппаратные ресурсы и интерфейс ВМ:](https://github.com/dlomov/sysadm-homeworks/blob/master/03-sysadmin-01-terminal/vm1.PNG)

6. Ознакомьтесь с возможностями конфигурации VirtualBox через Vagrantfile: [документация](https://www.vagrantup.com/docs/providers/virtualbox/configuration.html). Как добавить оперативной памяти или ресурсов процессора виртуальной машине?

Редактирования `Vagrantfile`
```bash
Vagrant.configure("2") do |config|
	config.vm.box = "bento/ubuntu-20.04"
		config.vm.provider "virtualbox" do |v|
			v.gui = false #отключил GUI
			v.name = "Ubuntu-20.04" #добавил имя вм
			v.linked_clone = true #включил ссылку на клон
			v.customize ["modifyvm", :id, "--cpuexecutioncap", "50"] #ресурс CPU до 50%
			v.memory = 2048 #изменил RAM до 2GB
			v.cpus = 2 #кол-во CPU
		end
end
```
Или вводим команды `комманд` из документации
```bash
config.vm.provider "virtualbox" do |v|
  v.name = "my_vm" #сменить имя
end
```
7. Команда `vagrant ssh` из директории, в которой содержится Vagrantfile, позволит вам оказаться внутри виртуальной машины без каких-либо дополнительных настроек. Попрактикуйтесь в выполнении обсуждаемых команд в терминале Ubuntu.
```bash
 vagrant ssh
Welcome to Ubuntu 20.04.4 LTS (GNU/Linux 5.4.0-110-generic x86_64) 

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Fri 17 Jun 2022 02:24:33 PM UTC

  System load:  0.0                Processes:             123      
  Usage of /:   11.9% of 30.63GB   Users logged in:       0        
  Memory usage: 9%                 IPv4 address for eth0: 10.0.2.15
  Swap usage:   0%


This system is built by the Bento project by Chef Software
More information can be found at https://github.com/chef/bento
vagrant@vagrant:~$ 
```

8. Ознакомиться с разделами `man bash`, почитать о настройках самого bash:
    * какой переменной можно задать длину журнала `history`, и на какой строчке manual это описывается?
	```
	HISTFILESIZE — максимальное число строк в файле истории для сохранения, строка 703.
	HISTSIZE — число команд для сохранения, строка 715
	```
    * что делает директива `ignoreboth` в bash?
	```
	Не записывать команду, которая начинается с пробела, либо команду, которая дублирует предыдущую. 
	ignoreboth — это сокращение для 2х директив:
	ignorespace — не сохранять команды начинающиеся с пробела, 
    ignoredups — не сохранять команду, если такая уже имеется в истории.
	```
9. В каких сценариях использования применимы скобки `{}` и на какой строчке `man bash` это описано?
```
{} - зарезервированные слова, список, в т.ч. список команд команд в отличии от "(...)" исполнятся в текущем инстансе, используется в различных условных циклах, условных операторах, или ограничивает тело функции, 
В командах выполняет подстановку элементов из списка , если упрощенно то  цикличное выполнение команд с подстановкой 
например mkdir ./DIR_{A..Z} - создаст каталоги сименами DIR_A, DIR_B и т.д. до DIR_Z.
Строка 343.
```
10. Основываясь на предыдущем вопросе, как создать однократным вызовом `touch` 100000 файлов? 
```bash
vagrant@vagrant:~/files$ touch {000001..100000} 2> err-files #создали 100000 файлов
vagrant@vagrant:~/files$ ls -f  | wc -l #быстро посчитали
100000
```
А получилось ли создать 300000? Если нет, то почему?

Создать `300000 файлов` не получилось, слишком `длинный аргумент`.
```bash
vagrant@vagrant:~/files$ touch {000001..300000} 2> err-files
vagrant@vagrant:~/files$ cat err-files
-bash: /usr/bin/touch: Argument list too long
```
11. В man bash поищите по `/\[\[`. Что делает конструкция `[[ -d /tmp ]]`?

Конструкция `[[ -d /tmp ]]` ищет директиву `tmp` на `диске d`
```bash
17:36:46 vagrant@vagrant(0):~$ if [[ -d /tmp ]]; then echo "директория есть"; else echo "директории нет";  fi
директория есть
```
12. Основываясь на знаниях о просмотре текущих (например, PATH) и установке новых переменных; командах, которые мы рассматривали, добейтесь в выводе type -a bash в виртуальной машине наличия первым пунктом в списке:

	```bash
	bash is /tmp/new_path_directory/bash
	bash is /usr/local/bin/bash
	bash is /bin/bash
	```

	(прочие строки могут отличаться содержимым и порядком)
    В качестве ответа приведите команды, которые позволили вам добиться указанного вывода или соответствующие скриншоты.
```bash
17:45:14 vagrant@vagrant(0):~$ mkdir /tmp/new_path_directory/
17:47:03 vagrant@vagrant(0):~$ cp /tmp/new_path_directory/
17:47:36 vagrant@vagrant(0):~$ cp /bin/bash /tmp/new_path_directory/
17:48:12 vagrant@vagrant(0):~$ type -a bash
bash is /usr/bin/bash
bash is /bin/bash
17:48:16 vagrant@vagrant(0):~$ PATH=/tmp/new_path_directory/:$PATH
17:48:37 vagrant@vagrant(0):~$ type -a bash
bash is /tmp/new_path_directory/bash
bash is /usr/bin/bash
bash is /bin/bash
```

13. Чем отличается планирование команд с помощью `batch` и `at`?

`at` — выполняет команды в указанное время,
`batch` — выполняет команды, если уровень загрузки системы падает ниже 1.5, или ниже значения указанного в atd.

14. Завершите работу виртуальной машины чтобы не расходовать ресурсы компьютера и/или батарею ноутбука.
```bash
$ vagrant suspend
==> default: Saving VM state and suspending execution...
```



---
