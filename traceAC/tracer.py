"""Этот модуль реализует логику трассировщика"""
import re
import sys
import socket
from subprocess import check_output, CalledProcessError

try:
    import requests
except ImportError:
    sys.exit('Module "requests" not found')

WHOISSERVERS = ['whois.ripe.net', 'whois.apnic.net', 'whois.afrinic.net', 'whois.arin.net', 'whois.lacnic.net']

READY = re.compile('трассировка завершена', flags=re.IGNORECASE)
RESERVED = re.compile(b'reserved:\w*', flags=re.IGNORECASE)
COUNTRY = re.compile(b'country:\s*\w+\n', flags=re.IGNORECASE)
ORIGIN_AS = re.compile(b'origin[a-z]*:\s*\w+\n', flags=re.IGNORECASE)
AS_LACNIC = re.compile(b'aut-num:\s*\w+\n', flags=re.IGNORECASE)
PROVIDER = re.compile(b'class="isp">[\w\W]*?</p>', flags=re.IGNORECASE)
IP = re.compile('\d+.\d+.\d+.\d+')


class Tracer:
    """Класс трассирвщика"""

    def __init__(self, tracing_address):
        """Конструктор класса"""
        self._tracing_address = tracing_address
        self._ready_ip = []
        self._tracing()

    def __str__(self):
        """Переопределение метода вывода"""
        result = '\n' + ' №'.ljust(6, ' ') + 'IP'.ljust(22, ' ') + 'AS'.ljust(15, ' ') + 'Country'.ljust(14) + \
                 'Provider' + '\n'
        counter = 1
        max_length = 0
        for ip in self._ready_ip:
            if len(ip.provider) > max_length:
                max_length = len(ip.provider)
        result = result + ' '.ljust(58 + max_length, '-') + '\n'
        for ip in self._ready_ip:
            result = result + ' ' + str(counter).zfill(2) + ":  " + ip.__str__()
            counter += 1
        return result

    def _tracing(self):
        """Трассировка до указанного адреса (только IPv4)"""
        print(f'> Tracing to the {self._tracing_address}. Wait...')
        try:
            data = check_output(['tracert', '-d', '-w', '1000', '-4', self._tracing_address]).decode('cp866')
            result = re.findall(READY, data)
            if len(result) != 0:
                self._find_info(self._find_ip_addresses(data))
            else:
                raise TracerError('Tracing was not completed. Some problem.')
        except CalledProcessError:
            print(f'> Tracing was not completed. Some problem.')
            sys.exit()

    def _find_ip_addresses(self, data):
        """Поиск IP адресов из полученный данных"""
        ip_addresses = []
        found_ip = re.findall(IP, data)
        if len(found_ip) == 1:
            raise TracerError('Tracing did not find any IP.')
        self._destination = found_ip.pop(0)
        for ip in found_ip:
            ip_addresses.append(ip)
        return ip_addresses

    def _find_info(self, ip_addresses):
        """Поиск данных на серверах whois"""
        print('> Obtaining information about IP addresses...')
        for ip in ip_addresses:
            self._ready_ip.append(get_ip_info(ip))


class TracerError(Exception):
    """Ошибка, возникающая при ошибках трассировки"""
    pass


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


def get_ip_info(ip):
    """Получить информацию об IP адресе"""
    country = None
    origin_as = None
    for server in WHOISSERVERS:
        data = _get_data_from_socket(server, ip)
        reserved = re.findall(RESERVED, data)
        if len(reserved) != 0:
            return IPDescription(ip, 'Reserved', 'Reserved', 'Reserved')
        result_country = re.findall(COUNTRY, data)
        if len(result_country) != 0:
            country = result_country[0][8:-1].strip()
            country = country.decode()
        result_as = re.findall(ORIGIN_AS, data)
        if len(result_as) != 0:
            origin_as = result_as[0][9:-1].strip()
            origin_as = origin_as.decode()
        result_as = re.findall(AS_LACNIC, data)
        if len(result_as) != 0:
            origin_as = result_as[0][9:-1].strip()
            origin_as = origin_as.decode()
        if country is not None and origin_as is not None:
            break
    if country is None:
        country = "Unknown"
    if origin_as is None:
        origin_as = 'Unknown'
    provider = _get_provider(ip)
    return IPDescription(ip, origin_as, country, provider)


def _get_data_from_socket(server, ip):
    """Получить данные об IP из сокета"""
    data = b''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as request_socket:
        request_socket.connect((server, 43))
        request_socket.send(ip.encode('ASCII') + b'\r\n')
        file = request_socket.makefile('rb')
        line = file.readline()
        while line != b'':
            data += line
            line = file.readline()
    return data


def _get_provider(ip):
    """Получить провайдера по IP"""
    address = 'https://www.whoismyisp.org/ip/' + str(ip)
    response = requests.get(address)
    provider = re.findall(PROVIDER, response.content)[0].decode(response.encoding)[12:-4]
    if provider is None or provider == '':
        return 'Unknown'
    return provider
