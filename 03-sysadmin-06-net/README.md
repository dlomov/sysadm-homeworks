# Домашнее задание к занятию "3.6. Компьютерные сети, лекция 1"

1. Работа c HTTP через телнет.
- Подключитесь утилитой телнет к сайту stackoverflow.com
`telnet stackoverflow.com 80`
- отправьте HTTP запрос
	```bash
	GET /questions HTTP/1.0
	HOST: stackoverflow.com
	[press enter]
	[press enter]
	```
	```bash
	vagrant@vagrant:~$ telnet stackoverflow.com 80
	Trying 151.101.193.69...
	Connected to stackoverflow.com.
	Escape character is '^]'.
	GET /questions HTTP/1.0
	HOST: stackoverflow.com

	HTTP/1.1 301 Moved Permanently
	Server: Varnish
	Retry-After: 0
	Location: https://stackoverflow.com/questions
	Content-Length: 0
	Accept-Ranges: bytes
	Date: Sun, 28 Aug 2022 10:09:21 GMT
	Via: 1.1 varnish
	Connection: close
	X-Served-By: cache-ams21062-AMS
	X-Cache: HIT
	X-Cache-Hits: 0
	X-Timer: S1661681362.712444,VS0,VE0
	Strict-Transport-Security: max-age=300
	X-DNS-Prefetch-Control: off

	Connection closed by foreign host.
	```
- В ответе укажите полученный HTTP код, что он означает?
### Ответ
В ответ пришел HTTP код 301: это редиект на другой URL, он указан в поле location. В даном случае, адрес тот же, но протокол HTTPS.

2. Повторите задание 1 в браузере, используя консоль разработчика F12.
- откройте вкладку `Network`
- отправьте запрос http://stackoverflow.com
- найдите первый ответ HTTP сервера, откройте вкладку `Headers`
- укажите в ответе полученный HTTP код.
- проверьте время загрузки страницы, какой запрос обрабатывался дольше всего?
- приложите скриншот консоли браузера в ответ.
### Ответ
301 Moved Permanently, время загрузки 1.40 сек, дольше всего обрабатывался документ questions 429мс.

![время:](https://github.com/dlomov/sysadm-homeworks/blob/master/03-sysadmin-06-net/301.PNG)
![время:](https://github.com/dlomov/sysadm-homeworks/blob/master/03-sysadmin-06-net/time.PNG)

3. Какой IP адрес у вас в интернете?

	```bash
	vagrant@vagrant:~$ wget -qO- eth0.me
	xxx.xxx.xxx.xxx
	```
4. Какому провайдеру принадлежит ваш IP адрес? Какой автономной системе AS? Воспользуйтесь утилитой `whois`

	```bash
	vagrant@vagrant:~$ whois xxx.xxx.xxx.xxx  | grep -P '^org-name|^origin'
	org-name:       Hosting technology LTD
	origin:         AS207651
	```
5. Через какие сети проходит пакет, отправленный с вашего компьютера на адрес 8.8.8.8? Через какие AS? Воспользуйтесь утилитой `traceroute`

	```bash
	vagrant@vagrant:~$ traceroute -I -An 8.8.8.8
	traceroute to 8.8.8.8 (8.8.8.8), 30 hops max, 60 byte packets
	1  10.0.2.2 [*]  0.463 ms  0.393 ms  0.349 ms
	2  * * *
	3  xxx.189.224.1 [AS207651]  6.849 ms  8.825 ms  8.784 ms
	7  xx.14.205.132 [AS207651]  49.509 ms  46.628 ms  47.941 ms
	8  xx.170.250.129 [AS15169]  49.904 ms  50.455 ms  50.415 ms
	9  xx.170.250.130 [AS15169]  47.765 ms  47.566 ms  50.580 ms
	10  xx.250.238.214 [AS15169]  70.980 ms  75.542 ms  75.491 ms
	11  xxx.250.235.68 [AS15169]  66.060 ms  70.805 ms  61.480 ms
	12  xxx.250.56.219 [AS15169]  62.323 ms  62.921 ms  61.899 ms
	22  8.8.8.8 [AS15169]  67.072 ms  61.082 ms  61.148 ms

	vagrant@vagrant:~$ grep org-name <(whois AS207651)
	org-name:       Hosting technology LTD
	vagrant@vagrant:~$ grep orgname <(whois AS15169) -i
	OrgName:        Google LLC
	```
6. Повторите задание 5 в утилите `mtr`. На каком участке наибольшая задержка - delay?
### Ответ

Наибольшая задержка на участке 2 AS15169

```bash
vagrant@vagrant:~$ mtr 8.8.8.8 -znrc 1 --tcp
Start: 2022-08-28T13:08:29+0000
HOST: vagrant                Loss%   Snt   Last   Avg  Best  Wrst StDev
1. AS???    10.0.2.2       0.0%     1    0.3   0.3   0.3   0.3   0.0
2. AS15169  8.8.8.8        0.0%     1    1.1   1.1   1.1   1.1   0.0

```


7. Какие DNS сервера отвечают за доменное имя dns.google? Какие A записи? воспользуйтесь утилитой `dig`

	```bash
	vagrant@vagrant:~$ dig +short NS dns.google A dns.google
	;; Warning, extra type option
	8.8.4.4
	8.8.8.8
	ns4.zdns.google.
	ns3.zdns.google.
	ns2.zdns.google.
	ns1.zdns.google.
	```
8. Проверьте PTR записи для IP адресов из задания 7. Какое доменное имя привязано к IP? воспользуйтесь утилитой `dig`

	```bash
	vagrant@vagrant:~$ for ip in `dig +short A dns.google`; do dig -x $ip | grep ^[0-9].*in-addr; done
	8.8.8.8.in-addr.arpa.   4941    IN      PTR     dns.google.
	4.4.8.8.in-addr.arpa.   78794   IN      PTR     dns.google.
	```

---