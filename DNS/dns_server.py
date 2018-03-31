from dns_packet import *
import datetime
import socket

class DNSServer:
    """Класс SNTP сервера"""

    def __init__(self, host, port, time_shift=0):
        """Конструктор"""
        self._host = host  # Адресс хоста
        self._port = port  # Номер порта
        self._time_shift = time_shift  # Временной сдвиг

    @property
    def host(self):
        return self._host

    @property
    def port(self):
        return self._port

    @property
    def time_shift(self):
        return self._time_shift

    def _create_connection(self):
        """Создать подключение к сокету"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.socket.settimeout(1 / 60)
            self.socket.bind((self.host, self.port))
            self.reply_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print(f'> {datetime.datetime.now()} SNTP Server was start. (HOST: {self.host}, PORT: {self.port})')
        except OSError as exception:
            print(f'> {datetime.datetime.now()} ERROR! SNTP server was not start. {exception}')

    def start_server(self):
        """Запустить сервер"""
        self._create_connection()
        while True:
            try:
                data, address = self.socket.recvfrom(1024)
                print(f'> {datetime.datetime.now()} Received request from: (HOST: {address[0]}, PORT: {address[1]})')
            except socket.timeout:
                continue
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as reply_socket:
                    reply_socket.connect(('ns1.e1.ru', 53))
                    reply_socket.sendall(data)
                    rec = reply_socket.recv(2048)
                    #read(data)
                    read(rec)
            except Exception as exception:
                print(f'> {datetime.datetime.now()} Packet from: (HOST: {address[0]}, PORT: {address[1]}) '
                      'was dropped, some problem: {}'.format(exception))
                continue

    def stop_server(self):
        """Остановить работу сервера"""
        self.socket.close()
        print(f'> {datetime.datetime.now()} Server was stop')