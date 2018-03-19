import argparse
import sys
from sntp_server import *

__version__ = "1.0"
__author__ = "Gridin Andrey"


def args_parser():
    """Парсер аргументов командной строки"""
    parser = argparse.ArgumentParser(description="SNTP server that is 'lying' for specified number of seconds")
    parser.add_argument('-t', '--time-shift', type=int, default=0, help='Time shift')
    return parser.parse_args()


def main():
    """Точка входа"""
    args = args_parser()
    server = SNTPServer('127.0.0.1', 123, args.time_shift)
    try:
        server.start_server()
    except KeyboardInterrupt:
        server.stop_server()
        sys.exit()
    except Exception as exception:
        print(exception)
    finally:
        server.stop_server()
        sys.exit()


if __name__ == "__main__":
    main()