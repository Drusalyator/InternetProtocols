import argparse
import sys
from dns_server import *


def main():
    """Точка входа"""
    server = DNSServer('127.0.0.1', 53)
    server.start_server()


if __name__ == "__main__":
    main()