import argparse
import sys
from dns_server import *

__version__ = "1.0"
__author__ = "Gridin Andrey"


def main():
    """Точка входа"""
    server = DNSServer()
    server.start_server()


if __name__ == "__main__":
    main()
