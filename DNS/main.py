import argparse
import sys
from dns_server import *


def main():
    """Точка входа"""
    server = DNSServer()
    server.start_server()


if __name__ == "__main__":
    main()
