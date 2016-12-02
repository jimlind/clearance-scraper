#!/usr/bin/python
from colorama import Fore, Back, Style

def success(seconds, proxyUrl):
    message = Fore.GREEN + ' SUCCESS!' + Style.RESET_ALL + ' | '
    message += Fore.WHITE + Back.GREEN + Style.BRIGHT + (' ' + seconds + 's ').ljust(12) + Style.RESET_ALL + ' | '
    message += proxyUrl
    print message

def failure(seconds, proxyUrl):
    message = Fore.RED + ' FAILURE!' + Style.RESET_ALL + ' | '
    message += Fore.WHITE + Back.RED + Style.BRIGHT + ('').ljust(12) + Style.RESET_ALL + ' | '
    message += proxyUrl
    print message
