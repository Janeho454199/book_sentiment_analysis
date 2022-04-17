#!/usr/bin/env python
"""
-------------------------------------------------
   开发人员：janeho
   开发日期：2022-03-04
   开发工具：PyCharm
   功能描述：日志组件
-------------------------------------------------
    Change Activity:

-------------------------------------------------
"""
import logging
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)


class Logger:
    """
    Token from https://github.com/gaojiuli/toapi/blob/master/toapi/log.py
    """

    def __init__(self, name, level=logging.DEBUG):
        logging.basicConfig(format='%(asctime)s %(message)-10s ',
                            datefmt='%Y/%m/%d %H:%M:%S')

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

    def info(self, type, message, color=Fore.CYAN):
        self.logger.info(color + '[%-16s] %-2s %s' % (type, 'OK', message) + Style.RESET_ALL)

    def error(self, type, message, color=Fore.RED):
        self.logger.error(color + '[%-16s] %-4s %s' % (type, 'FAIL', message) + Style.RESET_ALL)

    def exception(self, type, message, color=Fore.RED):
        self.logger.error(color + '[%-16s] %-5s %s' % (type, 'ERROR', message) + Style.RESET_ALL)


logger = Logger('spdier')
