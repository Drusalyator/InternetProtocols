"""Этот модуль реализует логику трассировщика"""
import re
from subprocess import check_output, CalledProcessError

try:
    import requests
    import json
except ImportError:
    sys.exit('Module "requests" not found')

IP_REG = re.compile('\d+.\d+.\d+.\d+')
AS_REG = re.compile('AS\d+')
READY = re.compile('трассировка завершена', flags=re.IGNORECASE)


def tracing(tracing_address):
    """Трассировка до указанного адреса (только IPv4)"""
    print(f'> Tracing to the {tracing_address}. Wait...')
    try:
        data = check_output(['tracert', '-d', '-w', '400', '-4', tracing_address]).decode('cp866')
        result = re.findall(READY, data)
        if len(result) != 0:
            print_info(_find_info(_find_ip_addresses(data)))
        else:
            raise TracerError('Tracing was not completed. Some problem.')
    except CalledProcessError:
        print(f'> Tracing was not completed. Some problem.')
        sys.exit()


def _find_ip_addresses(data):
    """Поиск IP адресов из полученный данных"""
    ip_addresses = []
    found_ip = re.findall(IP_REG, data)
    if len(found_ip) == 1:
        raise TracerError('Tracing did not find any IP.')
    found_ip.pop(0)
    for ip in found_ip:
        ip_addresses.append(str(ip).strip())
    return ip_addresses


def _find_info(ip_addresses):
    """Поиск данных на серверах whois"""
    print('> Obtaining information about IP addresses...')
    ready_ip = []
    for ip in ip_addresses:
        response = requests.get('http://ip-api.com/json/' + ip)
        answer = json.loads(response.content)
        if answer['status'] == 'success':
            ip = IPDescription(ip, re.findall(AS_REG, answer['as'])[0], answer['countryCode'], answer['isp'])
        else:
            ip = IPDescription(ip, 'Reserved', 'Reserved', 'Reserved')
        ready_ip.append(ip)
    return ready_ip


def print_info(ready_ip):
    """Напечать результат в консоль"""
    result = '\n' + ' №'.ljust(6, ' ') + 'IP'.ljust(22, ' ') + 'AS'.ljust(15, ' ') + 'Country'.ljust(14) + \
             'Provider' + '\n'
    counter = 1
    max_length = 0
    for ip in ready_ip:
        if len(ip.provider) > max_length:
            max_length = len(ip.provider)
    result = result + ' '.ljust(58 + max_length, '-') + '\n'
    for ip in ready_ip:
        result = result + ' ' + str(counter).zfill(2) + ":  " + ip.__str__()
        counter += 1
    print(result)


class IPDescription:
    """Класс описания IP адреса"""

    def __init__(self, ip, origin_as, country, provider):
        """Конструктор"""
        self.ip = ip
        self.origin_as = origin_as
        self.country = country
        self.provider = provider

    def __str__(self):
        """Переопределение метода вывода"""
        result = f'{self.ip}'.ljust(22, ' ') + f'{self.origin_as}'.ljust(15, ' ') + \
                 f'{self.country}'.ljust(14, ' ') + f'{self.provider}\n'
        return result
