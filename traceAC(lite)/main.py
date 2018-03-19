"""Этот модуль реализует логику трассировщика"""
import argparse
import sys

try:
    from tracer import *
except ImportError:
    sys.exit('Some program module not found')

__version__ = '1.0'
__author__ = 'Gridin Andrey'


def parse_args():
    """Парсер аргуметов"""
    parser = argparse.ArgumentParser(description="Tracing with AS, country and provider")
    parser.add_argument("-a", "--address", help="Address for tracing")
    return parser.parse_args()


def input_ip_or_domain_name():
    """Вести IP или доменное имя"""
    address = input("> Input IP or domain name: ").strip()
    while address == '':
        address = input("> Input IP or domain name: ").strip()
    return address


def main():
    """Точка входа"""
    try:
        args = parse_args()
        if args.address is not None:
            address = args.address
        else:
            address = input_ip_or_domain_name()
        tracing(address)
    except Exception as exception:
        print("> Error! {}".format(exception))


if __name__ == "__main__":
    main()
