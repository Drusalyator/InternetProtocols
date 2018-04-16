import collections
import socket
import sys
import concurrent.futures as cf
from threading import Thread

try:
    from dns_packet import *
    from dns_cache import *
except ImportError:
    sys.exit('Program module not found')


class DNSServer:
    """Класс SNTP сервера"""

    def __init__(self, host='127.0.0.2', port=53, main_server='ns1.e1.ru.'):
        """Конструктор"""
        self._host = host                           # Адресс хоста
        self._port = port                           # Номер порта
        self._main_server = main_server             # Сервер, откуда будем брать информацию
        self._frame_queue = collections.deque([])   # Очередь задач
        self._cache = Cache()                       # Кэш

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def main_server(self):
        return self._main_server

    @property
    def frame_queue(self):
        return self._frame_queue

    def _create_connection(self):
        """Создать подключение к сокету"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.settimeout(1 / 60)
            self.socket.bind((self.host, self.port))
            print(f'> {datetime.now()} > DNS Server was start. (HOST: {self.host}, PORT: {self.port})\n')
        except OSError as exception:
            print(f'> {datetime.now()} > ERROR! DNS server was not start. {exception}')
            sys.exit()

    def _receive_frame(self):
        """Создать подключение, получать данные и отправлять ответ"""
        self._create_connection()
        while True:
            try:
                frame, address = self.socket.recvfrom(1024)
                print(f'> {datetime.now()} > Received request from: (HOST: {address[0]}, PORT: {address[1]})')
            except socket.timeout:
                continue
            if frame:
                try:
                    cache_answer = self._cache.find_entry(read_dns_packet(frame))
                    if cache_answer is None:
                        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
                            try:
                                server_socket.settimeout(3)
                                server_socket.bind(('', 0))
                                server_socket.sendto(frame, (self.main_server, self.port))
                                answer = server_socket.recvfrom(1024)[0]
                            except OSError:
                                answer = None
                    else:
                        answer = cache_answer.to_bytes()
                    if answer:
                        answer_packet = read_dns_packet(answer)
                        self.socket.sendto(answer_packet.to_bytes(), address)
                        print(
                            f'> {datetime.now()} > Reply was sent on address (HOST: {address[0]}, PORT: {address[1]})')
                        self._cache.add_entry(answer_packet)
                except DNSPacketError:
                    print(f'> {datetime.now()} > Some problem. Unsupported frame format. Packet was dropped')

    def start_server(self):
        """Запусть сервер"""
        try:
            load_cache_from_file(self._cache)
            print(f"> {datetime.now()} > Cache was loaded from file 'dns.cache'\n")
        except Exception as exception:
            print(f"> {datetime.now()} > Could not load cache from file : {exception}\n")
        try:
            self._receive_frame()
        except KeyboardInterrupt:
            self.socket.close()
            try:
                save_cache_in_file(self._cache)
                print(f"> {datetime.now()} > Cache was saved in file: 'dns.cache'")
            except Exception as exception:
                print(f"> {datetime.now()} > Could not save the cache: {exception}")
            print(f'> {datetime.now()} > Server was stop')
            sys.exit()
