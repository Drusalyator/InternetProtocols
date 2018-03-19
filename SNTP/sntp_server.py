import datetime
import socket
from sntp_packet import *


class SNTPServer:
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
                receive_timestamp = datetime.datetime.now().timestamp()
                print(f'> {datetime.da     tetime.now()} Received request from: (HOST: {address[0]}, PORT: {address[1]})')
            except socket.timeout:
                continue
            try:
                request_message = SNTPPacket()
                request_message.read_packet(data)
                originate_timestamp = request_message.transmit_timestamp
                li = request_message.li
                vn = request_message.vn
                transmit_timestamp = datetime.datetime.now().timestamp()
                reply_message = pack_packet(li=li, vn=vn, originate_timestamp=originate_timestamp,
                                            receive_timestamp=receive_timestamp,
                                            transmit_timestamp=transmit_timestamp, time_shift=self.time_shift)
                self.reply_socket.sendto(reply_message, address)
                print(f'> {datetime.datetime.now()} Reply was send to: (HOST: {address[0]}, PORT: {address[1]})')
            except Exception as exception:
                print(f'> {datetime.datetime.now()} Packet from: (HOST: {address[0]}, PORT: {address[1]}) '
                      'was dropped, some problem: {}'.format(exception))
                continue

    def stop_server(self):
        """Остановить работу сервера"""
        self.socket.close()
        print(f'> {datetime.datetime.now()} Server was stop')
