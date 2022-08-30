# Домашнее задание к занятию "3.9. Элементы безопасности информационных систем"

1. Установите Bitwarden плагин для браузера. Зарегестрируйтесь и сохраните несколько паролей.
2. Установите Google authenticator на мобильный телефон. Настройте вход в Bitwarden акаунт через Google authenticator OTP.

![2FA:](https://github.com/dlomov/sysadm-homeworks/blob/master/03-sysadmin-09-security/2FA.PNG)

3. Установите apache2/nginx, сгенерируйте самоподписанный сертификат, настройте тестовый сайт для работы по HTTPS.
### Установим nginx
```
sudo apt update
sudo apt install nginx -y
```
### Настроим брандмауэр
Прежде чем запустить Nginx, нужно настроить брандмауэр для поддержки трафика этого сервиса. У меня Ubuntu 20.04, установлю и настрою ufw.
```bash
sudo apt install ufw
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw enable
sudo ufw status verbose
sudo ufw app list
Available applications:
Nginx Full
Nginx HTTP
Nginx HTTPS
OpenSSH
```
- Nginx Full: этот профиль открывает порт 80 (незашифрованный сетевой трафик) и 443 (зашифрованный трафик TLS/SSL).
- Nginx HTTP: профиль для незашифрованного трафика HTTP на порт 80.
- Nginx HTTPS: профиль для зашифрованного трафика TLS/SSL на порт 443.
Включим
```
sudo ufw allow 'Nginx Full'
```
### Создам SSL-сертификат
Чтобы создать самоподписанный сертификат и ключ, запустите команду:
```bash
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/nginx-selfsigned.key -out /etc/ssl/certs/nginx-selfsigned.crt
sudo openssl dhparam -out /etc/nginx/dhparam.pem 409
```
[подробнее об установке](https://www.8host.com/blog/sozdanie-samopodpisannogo-ssl-sertifikata-dlya-nginx-v-ubuntu-18-04/)

Проверим сертификат
Убедимся что работает https и проверим сертификат
```bash
vagrant@vagrant:~$ curl -k https://localhost
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
vagrant@vagrant:~$ 
```
```bash
vagrant@vagrant:~$ echo | openssl s_client -showcerts -servername localhost -connect localhost:443 2>/dev/null | openssl x509 -inform pem -noout -text
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            fb:b8:62:8f:2e:33:1a:f0:43:c8:90:4d:54:b2:d0:44:bf:21:6a
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: C = AU, ST = Some-State, O = Internet Widgits Pty Ltd
        Validity
            Not Before: Aug 29 14:19:15 2022 GMT
            Not After : Aug 29 14:19:15 2023 GMT
        Subject: C = AU, ST = Some-State, O = Internet Widgits Pty Ltd
        Subject Public Key Info:
            Public Key Algorithm: rsaEncryption
                RSA Public-Key: (2048 bit)
                Modulus:
                    00:b7:7f:ec:04:08:9d:a5:50:b0:26:98:14:6a:9d:
                    16:2d:6b:b3:a6:d8:4c:b4:d1:12:a2:8d:db:12:c1:
                    36:84:f7:44:ae:10:33:90:83:9f:f5:82:fb:39:6b:
                    f6:5c:6c:25:e0:7c:01:67:c7:f6:9f:5f:f5:3b:fb:
                    70:8b:68:dd:7d:d5:da:99:32:95:7e:b1:df:b6:6a:
                    0a:84:36:85:e9:c3:fb:21:db:e7:91:03:59:81:f0:
                    a4:d5:a3:bf:78:a0:ab:4b:79:0a:ef:aa:38:29:a6:
                    31:09:8d:f4:cc:da:8c:ad:4c:70:3d:b0:92:ad:30:
                    0a:47:1c:fe:34:fc:2f:82:35:01:b4:71:b1:f1:8a:
                    1e:da:3e:a4:fa:0c:c9:9b:b5:c1:f1:78:4b:c7:8c:
                    5a:b5:28:36:4b:bb:63:31:58:e7:1c:77:d2:06:d6:
                    71:1c:3f:56:7e:a8:a0:cb:81:69:df:ab:10:01:be:
                    f9:38:57:4e:87:20:bd:41:40:91:ee:1c:58:be:ec:
                    4d:21:5d:eb:92:9d:4d:5e:d2:d2:2c:cd:d0:63:bd:
                    f9:a3:bc:89:42:37:99:ae:11:6e:d6:fb:88:1f:b9:
                    6e:c9:61:ad:0e:56:63:b6:89:56:b4:2c:5c:5f:0c:
                    78:31:fc:50:68:08:9f:54:b6:dc:f3:a0:58:99:70:
                    1d:cb
                Exponent: 65537 (0x10001)
        X509v3 extensions:
            X509v3 Subject Key Identifier:
                ED:2E:26:61:71:50:3F:4E:BB:75:A4:F5:84:87:12:B5:96:54:09:3B
            X509v3 Authority Key Identifier:
                keyid:ED:2E:26:61:71:50:3F:4E:BB:75:A4:F5:84:87:12:B5:96:54:09:3B

            X509v3 Basic Constraints: critical
                CA:TRUE
    Signature Algorithm: sha256WithRSAEncryption
         1d:f9:dd:ec:6d:83:b4:e9:60:1b:40:bf:40:6c:c6:31:2f:c3:
         86:1e:4b:5b:c2:7e:66:b6:f6:10:6d:d9:30:77:46:0b:80:3b:
         ea:41:4e:a3:05:1c:2f:3d:a6:9f:10:5f:ad:74:64:1b:ab:1f:
         4d:59:35:17:0a:0e:c4:4f:5a:ed:73:b6:52:71:04:0a:44:86:
         df:19:d6:57:03:2b:7b:dc:f1:7b:d8:b7:9d:53:e2:af:d7:9a:
         bb:e6:4b:fa:c2:5d:2b:8e:a5:db:e8:91:12:8d:3f:00:09:e0:
         0d:23:a5:83:af:6a:2b:9e:37:05:46:31:b6:96:2d:52:28:a5:
         a3:d9:d4:4c:3c:ab:56:68:15:2a:ce:69:3e:ea:53:27:3d:ee:
         2c:08:ee:7b:8b:06:64:28:3a:03:bf:14:01:01:0f:c0:ac:5a:
         b9:66:46:41:71:9b:38:12:4a:5d:0e:ec:ac:8b:7b:bc:35:4d:
         38:4f:af:9c:6b:2f:59:f5:2d:8c:67:a4:ff:fd:52:95:12:23:
         ad:f7:ca:2e:38:96:d3:74:dc:b9:e6:9b:6a:e6:f2:3c:bb:1f:
         4a:d9:51:03:fc:14:fd:85:e2:5c:67:93:16:22:d6:35:cb:ab:
         1c:9f:4b:4b:30:2e:6f:12:91:f7:68:6b:8d:85:41:7e:f8:93:
         f4:df:36:32
```
4. Проверьте на TLS уязвимости произвольный сайт в интернете (кроме сайтов МВД, ФСБ, МинОбр, НацБанк, РосКосмос, РосАтом, РосНАНО и любых госкомпаний, объектов КИИ, ВПК ... и тому подобное).
```
vagrant@vagrant:~$ docker run --rm -ti  drwetter/testssl.sh -U --sneaky https://timeweb.com/

###########################################################
    testssl.sh       3.2rc1 from https://testssl.sh/dev/

      This program is free software. Distribution and
             modification under GPLv2 permitted.
      USAGE w/o ANY WARRANTY. USE IT AT YOUR OWN RISK!

       Please file bugs @ https://testssl.sh/bugs/

###########################################################

 Using "OpenSSL 1.0.2-chacha (1.0.2k-dev)" [~183 ciphers]
 on ecfcd559b141:/home/testssl/bin/openssl.Linux.x86_64
 (built: "Jan 18 17:12:17 2019", platform: "linux-x86_64")


 Start 2022-08-29 14:35:26        -->> 185.65.148.89:443 (timeweb.com) <<--

 Further IP addresses:   2a03:6f00:1:2::5c35:746b 
 rDNS (185.65.148.89):   --
 Service detected:       HTTP


 Testing vulnerabilities 

 Heartbleed (CVE-2014-0160)                not vulnerable (OK), no heartbeat extension
 CCS (CVE-2014-0224)                       not vulnerable (OK)
 Ticketbleed (CVE-2016-9244), experiment.  not vulnerable (OK)
 ROBOT                                     not vulnerable (OK)
 Secure Renegotiation (RFC 5746)           supported (OK)
 Secure Client-Initiated Renegotiation     not vulnerable (OK)
 CRIME, TLS (CVE-2012-4929)                not vulnerable (OK)
 BREACH (CVE-2013-3587)                    no gzip/deflate/compress/br HTTP compression (OK)  - only supplied "/" tested
 POODLE, SSL (CVE-2014-3566)               not vulnerable (OK)
 TLS_FALLBACK_SCSV (RFC 7507)              Downgrade attack prevention supported (OK)
 SWEET32 (CVE-2016-2183, CVE-2016-6329)    VULNERABLE, uses 64 bit block ciphers
 FREAK (CVE-2015-0204)                     not vulnerable (OK)
 DROWN (CVE-2016-0800, CVE-2016-0703)      not vulnerable on this host and port (OK)
                                           make sure you don't use this certificate elsewhere with SSLv2 enabled services, see
                                           https://search.censys.io/search?resource=hosts&virtual_hosts=INCLUDE&q=15167F9179AA8A4DE86BF6D5E00DBBFFFD705A165AF3239E18A429D55F5B7450
 LOGJAM (CVE-2015-4000), experimental      not vulnerable (OK): no DH EXPORT ciphers, no DH key detected with <= TLS 1.2
 BEAST (CVE-2011-3389)                     TLS1: ECDHE-RSA-AES128-SHA
                                                 AES128-SHA DES-CBC3-SHA
                                           VULNERABLE -- but also supports higher protocols  TLSv1.1 TLSv1.2 (likely mitigated)
 LUCKY13 (CVE-2013-0169), experimental     potentially VULNERABLE, uses cipher block chaining (CBC) ciphers with TLS. Check patches
 Winshock (CVE-2014-6321), experimental    not vulnerable (OK)
 RC4 (CVE-2013-2566, CVE-2015-2808)        no RC4 ciphers detected (OK)
 Done 2022-08-29 14:36:42 [  79s] -->> 185.65.148.89:443 (timeweb.com) <<--
```

5. Установите на Ubuntu ssh сервер, сгенерируйте новый приватный ключ. Скопируйте свой публичный ключ на другой сервер. Подключитесь к серверу по SSH-ключу.
Сгенерировал приватный ключ, публичный скопировал на vm vagrant2
```bash
vagrant@vagrant1:~$ ssh-keygen -t rsa -C "you@mail.com"
vagrant@vagrant1:~$ ssh-copy-id -i .ssh/id_rsa vagrant@192.168.1.22
```
Проверил ssh ключ, подключившись на vm vagrant2:
```bash
vagrant@vagrant1:~$ ssh vagrant@192.168.1.22
Welcome to Ubuntu 20.04.4 LTS (GNU/Linux 5.4.0-110-generic x86_64)

  System information as of Tue 30 Aug 2022 07:30:43 AM UTC

  System load:  0.01               Processes:             110
  Usage of /:   11.7% of 30.63GB   Users logged in:       0
  Memory usage: 10%                IPv4 address for eth0: 
  
  Swap usage:   0%                 IPv4 address for eth1: 192.168.1.22

This system is built by the Bento project by Chef Software
More information can be found at https://github.com/chef/bento
vagrant@vagrant2:~$
```
 
6. Переименуйте файлы ключей из задания 5. Настройте файл конфигурации SSH клиента, так чтобы вход на удаленный сервер осуществлялся по имени сервера.
```bash
vagrant@vagrant1:~$ sudo mv ~/.ssh/id_rsa ~/.ssh/id_rsa_netology
vagrant@vagrant1:~$ sudo nano ~/.ssh/config
Host vagrant2
        HostName 192.168.1.22
        User vagrant
        Port 22
        IdentityFile ~/.ssh/id_rsa_netology
vagrant@vagrant1:~$ ssh vagrant2
Welcome to Ubuntu 20.04.4 LTS (GNU/Linux 5.4.0-110-generic x86_64)
```

7. Соберите дамп трафика утилитой tcpdump в формате pcap, 100 пакетов. Откройте файл pcap в Wireshark.
```bash
vagrant@vagrant1:~$ sudo tcpdump -nnei any -c 100 -w 100.pcap
tcpdump: listening on any, link-type LINUX_SLL (Linux cooked v1), capture size 262144 bytes

100 packets captured
101 packets received by filter
0 packets dropped by kernel
```
![dump:](https://github.com/dlomov/sysadm-homeworks/blob/master/03-sysadmin-09-security/dump.PNG)
 ---
## Задание для самостоятельной отработки (необязательно к выполнению)

8*. Просканируйте хост scanme.nmap.org. Какие сервисы запущены?

9*. Установите и настройте фаервол ufw на web-сервер из задания 3. Откройте доступ снаружи только к портам 22,80,443


 ---