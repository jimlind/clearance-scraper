#!/usr/bin/python
from colorama import Fore, Back, Style

def success(seconds, proxyUrl):
    message = coloredText('GREEN', 'SUCCESS!') + ' | '
    message += coloredBackground('GREEN', seconds + 's') + ' | '
    message += proxyUrl
    print message

def failure(seconds, proxyUrl):
    message = coloredText('RED', 'FAILURE!') + ' | '
    message += coloredBackground('RED') + ' | '
    message += proxyUrl
    print message

def coloredText(color, text, length = 8):
    return getattr(Fore, color) + ' ' + text.ljust(length) + ' ' + Style.RESET_ALL

def coloredBackground(color, text = '', length = 10):
    return Fore.WHITE + getattr(Back, color) + Style.BRIGHT + ' ' + text.ljust(length) + ' ' + Style.RESET_ALL
