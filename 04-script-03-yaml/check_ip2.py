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
