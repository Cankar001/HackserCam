import colorama
from colorama import Back, Fore, Style


def debug(msg):
    print(f"{Style.BRIGHT}{Fore.CYAN}" + msg + f"{Style.RESET_ALL}")


def trace(msg):
    print(f"{Style.BRIGHT}{Fore.WHITE}" + msg + f"{Style.RESET_ALL}")


def error(msg):
    print(f"{Style.BRIGHT}{Fore.RED}" + "[ERROR]: " + msg + f"{Style.RESET_ALL}")


def critical(msg):
    print(
        f"{Style.BRIGHT}{Fore.RED}" + "[CRITICAL ERROR]: " + msg + f"{Style.RESET_ALL}"
    )


def info(msg):
    print(f"{Style.BRIGHT}{Fore.BLUE}" + msg + f"{Style.RESET_ALL}")


def warn(msg):
    print(f"{Style.BRIGHT}{Fore.YELLOW}" + "[WARNING]: " + msg + f"{Style.RESET_ALL}")


def success(msg):
    print(f"{Style.BRIGHT}{Fore.GREEN}" + msg + f"{Style.RESET_ALL}")
