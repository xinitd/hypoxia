import sys


RESET  = '\033[0m'
BOLD   = '\033[1m'
GREEN  = '\033[32m'
YELLOW = '\033[33m'
RED    = '\033[31m'
BLUE   = '\033[34m'


def _supports_color():
    return hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()


def info(msg):
    if _supports_color():
        print(f'{BLUE}{BOLD}[*]{RESET} {msg}')
    else:
        print(f'[*] {msg}')


def success(msg):
    if _supports_color():
        print(f'{GREEN}{BOLD}[+]{RESET} {msg}')
    else:
        print(f'[+] {msg}')


def warning(msg):
    if _supports_color():
        print(f'{YELLOW}{BOLD}[!]{RESET} {msg}')
    else:
        print(f'[!] {msg}')


def error(msg):
    if _supports_color():
        print(f'{RED}{BOLD}[-]{RESET} {msg}')
    else:
        print(f'[-] {msg}')
