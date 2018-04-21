"""Модуль реализующий логику работы клиента"""
import logging
import socket
import sys

try:
    import ssl
    HAVE_SSL = True
except ImportError:
    HAVE_SSL = False

__all__ = ["POP3Client", "POP3ClientError"]

POP3_PORT = 110  # Стандартный порт
POP3_SSL_PORT = 995  # SSL порт

CRLF = b'\r\n'


Commands = {"USER": ("AUTH",),
            "PASS": ("AUTH",),
            "QUIT": ("AUTH", "TRANSACTION")}


class POP3ClientError(Exception):
    """Ошибка, возникающая при неправильной работы команды"""
    pass


class POP3Client:
    """Класс клиента"""

    def __init__(self, host: str):
        """Контруктор"""
        self._host = host
        self._sock = self._create_socket()
        self._state = "NOTAUTH"
        self._create_connection()

    def _create_socket(self):
        """Создание сокета"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if HAVE_SSL:
                ssl_sock = ssl.wrap_socket(sock)
                ssl_sock.settimeout(1)
                self._port = POP3_SSL_PORT
                return ssl_sock
            else:
                sock.settimeout(1)
                self._port = POP3_PORT
                return sock
        except OSError as exception:
            print(f" > ERROR! Could not create a socket. {exception}.")
            sys.exit()

    def _create_connection(self):
        """Создание подключения"""
        try:
            self._sock.connect((self._host, self._port))
            try:
                self._get_response()
                self._state = "AUTH"
                print(f" > Successful connection to: {self._host}")
            except POP3ClientError:
                print(f" > Error connection to: {self._host}")
                sys.exit()
        except socket.timeout as exception:
            print(f" > ERROR! Could not create a connection: {exception}.")
            sys.exit()

    def _shutdown(self):
        """Закончить работу с клиентом"""
        self._sock.close()

    def _send_data(self, data: str):
        """Отправить данные в сокет"""
        self._sock.sendall(data.encode() + CRLF)

    def _read_data(self) -> str:
        """Прочитать данные из сокета"""
        result = b""
        while True:
            try:
                part_of_data = self._sock.recv(1024)
                if part_of_data is None or part_of_data == b"":
                    break
                result += part_of_data
            except socket.timeout:
                break
        return result.decode()

    def _get_response(self):
        """Получить ответ на команду"""
        response = self._read_data()
        if not response.startswith("+"):
            raise POP3ClientError("ERROR!" + response[4:])
        return response[4:]

    def _is_valid_command(self, command: str) -> bool:
        """Проверка того является ли команда выполнимой из данного состояния"""
        states = Commands.get(command, None)
        if states is None or self._state not in states:
            return False
        return True

    def _execute_command(self, command: str) -> str:
        """Отправить команду и получить ответ"""
        if self._is_valid_command(command[0:4].strip()):
            self._send_data(command)
            try:
                response = self._get_response()
                return response
            except POP3ClientError as error:
                return f"Command Error: {error}"
        else:
            return "Command Error: Wrong command or command can not be execute from this state"

    # POP3 Команды

    def user(self, user: str) -> str:
        """Команда USER"""
        return " > " + self._execute_command(f"USER {user}")

    def password(self, password: str) -> str:
        """Команда PASS"""
        response = self._execute_command(f"PASS {password}")
        if response.startswith("Command Error"):
            return " > " + response
        self._state = "TRANSACTION"
        return " > Successful authorization"

    def quit(self) -> str:
        """Команда QUIT"""
        response = " > " + self._execute_command("QUIT")
        self._shutdown()
        return response
