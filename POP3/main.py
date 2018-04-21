import sys

try:
    from client_core import *
except ImportError:
    print("> ERROR! Some program module not found")
    sys.exit()

__version__ = "1.0"
__author__ = "Gridin Andrey"


def main():
    """Точка входа"""
    client = POP3Client("pop.yandex.ru")
    print(client.user("TestForProtocol"))
    print(client.password("fylhtq1999"))
    print(client.quit())


if __name__ == "__main__":
    main()
