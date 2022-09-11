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
    # print(f'yaml_to_file, fmt = {fmt}')
    if fmt == "yaml":
        stream = yaml.dump(d, indent=2)
    if fmt == "json":
        j = json.loads(d)
        stream = yaml.dump(j, indent=2)
    # print(f"write to: {f_name}\ndata:\n{stream}")
    with open(f_name, 'w') as file:
        file.write(stream)
    print(f'Файл {f_name} записан')


def json_to_file(f_name, d, fmt):
    # print(f'json_to_file, fmt = {fmt}')
    if fmt == "json":
        stream = json.dumps(json.loads(d), indent=4)
    if fmt == "yaml":
        y = yaml.safe_load(d)
        stream = json.dumps(y, indent=2)
    # print(f"write to: {f_name}\ndata:\n{stream}")
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
