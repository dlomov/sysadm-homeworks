# Домашнее задание к занятию "4.3. Языки разметки JSON и YAML"

## Обязательные задания

1. Мы выгрузили JSON, который получили через API запрос к нашему сервису:
	```
    { "info" : "Sample JSON output from our service\t",
        "elements" :[
            { "name" : "first",
            "type" : "server",
            "ip" : 7175 
            },
            { "name" : "second",
            "type" : "proxy",
            "ip : 71.78.22.43
            }
        ]
    }
	```
  Нужно найти и исправить все ошибки, которые допускает наш сервис

- `:[` пропустили пробел между двоеточием и скобкой
- `"ip" : 7175` не дописали ip адрес 0.0.28.7
- `"ip : 71.78.22.43` пропустили скобки


	```
	{
		"info": "Sample JSON output from our service\t",
			"elements": [
			{
				"name": "first",
				"type": "server",
				"ip": 7175
			},
			{
				"name": "second",
				"type": "proxy",
				"ip": "71.78.22.43"
			}
		]
	}
	```

2. В прошлый рабочий день мы создавали скрипт, позволяющий опрашивать веб-сервисы и получать их IP. К уже реализованному функционалу нам нужно добавить возможность записи JSON и YAML файлов, описывающих наши сервисы. Формат записи JSON по одному сервису: { "имя сервиса" : "его IP"}. Формат записи YAML по одному сервису: - имя сервиса: его IP. Если в момент исполнения скрипта меняется IP у сервиса - он должен так же поменяться в yml и json файле.
```python
import socket
import time
import json
import yaml

hosts = {"drive.google.com": "192.168.0.1",
         "mail.google.com": "172.16.0.1", "google.com": "10.0.0.1"}

while True:
    try:
        with open('services.json', 'r+') as config_json, open('services.yaml', 'r+') as config_yaml:
            try:  # загружаем services.json
                hosts_json = json.load(config_json)
                print(f"Подгружен services.json")
                # вывод ошибки фоматирования
            except json.decoder.JSONDecodeError as e:
                print(f"Файл services.json в неверном формате.")
                exit()
                # загружаем services.yaml
            try:
                hosts_yaml = hosts_yaml = yaml.load(
                    config_yaml.read(), Loader=yaml.SafeLoader)
                print(f"Подгружен services.yaml")
                # вывод ошибки фоматирования
            except yaml.scanner.ScannerError as e:
                print(f"Файл services.yaml в неверном формате.")
                exit()
                # сравниваем yaml и json
            if hosts_yaml != hosts_json:
                print(
                    f"""\nСписки хостов в json и yaml отличаются:\n\nyaml: {hosts_yaml}\njson: {hosts_json}\n\nУдалите один или исправьте вручную. Потом запустит скрипт заново.\n""")
                exit()
            else:
                try:
                    hosts = hosts_yaml
                    while True:
                        for host in hosts:
                            cur_ip = hosts[host]
                            check_ip = socket.gethostbyname(host)
                            if check_ip != cur_ip:
                                print(
                                    f"""[ERROR] {host} IP mismatch: {cur_ip} {check_ip}""")
                                hosts[host] = check_ip
                                with open("services.json", 'w+') as write_json, open("services.yaml", 'w+') as write_yaml:
                                    write_json.write(
                                        json.dumps(hosts, indent=4))
                                    write_yaml.write(
                                        yaml.dump(hosts, indent=4))
                            else:
                                print(f"""{host} - {cur_ip}""")
                        time.sleep(2)
                except KeyboardInterrupt:
                    config_json.close
                    config_yaml.close
                    break
    except FileNotFoundError as e:  # если нет файла services, создаем
        print(f'Нет файла {e.filename}, создаём ')
        config = open(e.filename, 'w+')
        if config.name.endswith('.json'):
            try:
                config_yaml = open('services.yaml', 'r+').read()
                hosts_yaml = yaml.load(
                    config_yaml, Loader=yaml.SafeLoader)
                config.write(json.dumps(hosts_yaml, indent=4))
            except FileNotFoundError:
                config.write(json.dumps(hosts, indent=4))
            except:
                print('ERROR, файл services.yaml не создан')
                exit()
        elif config.name.endswith('yaml') or e.filename.endswith('yml'):
            try:
                config_json = open('services.json', 'r+')
                hosts_json = json.load(
                    config_json)
                config.write(yaml.dump(hosts_json, indent=4))
            except FileNotFoundError:
                config.write(json.dumps(hosts, indent=4))
            except:
                print('ERROR, файл services.json не создан')
                exit()
        config.read()

```
## Дополнительное задание (со звездочкой*) - необязательно к выполнению

Так как команды в нашей компании никак не могут прийти к единому мнению о том, какой формат разметки данных использовать: JSON или YAML, нам нужно реализовать парсер из одного формата в другой. Он должен уметь:
   * Принимать на вход имя файла
   * Проверять формат исходного файла. Если файл не json или yml - скрипт должен остановить свою работу
   * Распознавать какой формат данных в файле. Считается, что файлы *.json и *.yml могут быть перепутаны
   * Перекодировать данные из исходного формата во второй доступный (из JSON в YAML, из YAML в JSON)
   * При обнаружении ошибки в исходном файле - указать в стандартном выводе строку с ошибкой синтаксиса и её номер
   * Полученный файл должен иметь имя исходного файла, разница в наименовании обеспечивается разницей расширения файлов

```python
#!/usr/bin/env python3.9

import yaml
import json
import sys


def check_formats(string):
    f = {}
    try:
        j = json.loads(string)
        f['json'] = "valid"
        y = yaml.safe_load(string)
        f['yaml'] = "json"
    except json.decoder.JSONDecodeError as e:
        try:
            y = yaml.safe_load(string)
            f['yaml'] = "valid"
            try:
                json.dumps(y)
                f['json'] = "yaml"
            except json.decoder.JSONDecodeError as e3:
                m3 = e3.args[0]
                print(m3)
                f['json'] = "err"
            except TypeError as e3:
                m3 = e3.args[0]
                if m3.endswith('not list'):
                    json.dumps(y)
                    f['json'] = "yaml"
        except (yaml.parser.ParserError, yaml.scanner.ScannerError) as e2:
            f['yaml'] = "err"
            f['json'] = "err"
    return f


def yaml_to_file(f_name, d, fmt):
    if fmt == "yaml":
        stream = yaml.dump(d, indent=2)
    if fmt == "json":
        j = json.loads(d)
        stream = yaml.dump(j, indent=2)
    with open(f_name, 'w') as file:
        file.write(stream)
    print(f'Файл {f_name} записан')


def json_to_file(f_name, d, fmt):
    if fmt == "json":
        stream = json.dumps(json.loads(d), indent=4)
    if fmt == "yaml":
        y = yaml.safe_load(d)
        stream = json.dumps(y, indent=2)
    with open(f_name, 'w') as file:
        file.write(stream)
    print(f'Файл {f_name} записан')


def except_pprint(l, c, p, d, ex):
    d = d.split('\n')
    print(f"""
Не получилось разобрать {ex} файл, парсер остановился на строке {l+1}, символ {c+1}.

{d[l]}
{' ' * c}^

Суть проблемы: {p}
""")


args = sys.argv
source_file, ext, name, converted_file = '', '', '', ''
try:
    source_file = args[1]
    ext = source_file.split('.')[-1]
    name = source_file.split(f'.{ext}')[0]
    print(f'Исходный файл {source_file}')
    if ext == 'json':
        converted_file = f'{name}.yaml'
    elif ext == 'yaml' or ext == 'yml':
        converted_file = f'{name}.json'
    else:
        print(
            f"""Расширение ".{ext}" не поддерживается.\nПожалуйста, укажите файл JSON или YAML""")
except IndexError:
    print('Укажите имя файла в формате JSON или YAML')
    exit()

with open(source_file, 'r', encoding='utf_8') as file:
    data = file.read()
formats = check_formats(data)

if ext == 'json':
    if formats['json'] == "valid":
        yaml_to_file(converted_file, data, 'json')
    elif formats['json'] == "yaml":
        print(f'Файл {source_file} имеет формат yaml, переписываем')
        json_to_file(source_file, data, 'yaml')
        yaml_to_file(converted_file, data, 'yaml')
    else:
        try:
            json.loads(data)
        except json.decoder.JSONDecodeError as e:
            except_pprint(e.lineno-1, e.colno-1, e.args[0], data, ext)
elif ext == 'yaml':
    if formats['yaml'] == "valid":
        json_to_file(converted_file, data, 'yaml')
    elif formats['yaml'] == "json":
        print(f'Файл {source_file} имеет формат json, переписываем')
        yaml_to_file(source_file, data, 'json')
        json_to_file(converted_file, data, 'json')
    else:
        try:
            yaml.safe_load(data)
        except yaml.parser.ParserError as e:
            except_pprint(e.problem_mark.line,
                          e.problem_mark.column, e.problem, data, ext)
        except yaml.scanner.ScannerError as e:
            try:
                except_pprint(e.context_mark.line,
                              e.context_mark.column, e.problem, data, ext)
            except AttributeError:
                except_pprint(e.problem_mark.line,
                              e.problem_mark.column, e.problem, data, ext)
```
```bash
C:\VM\sysadm-homeworks\04-script-03-yaml>python converter.py services.json
Исходный файл services.json
Файл services.yaml записан
```
