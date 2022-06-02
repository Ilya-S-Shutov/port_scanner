"""Подключаемый модуль. Импортирует в main.py настройки логгеров."""

import logging


logging.basicConfig(level=logging.DEBUG)

access_logger = logging.getLogger('aiohttp.access')
access_handler = logging.SysLogHandler(address='/dev/log')
# access_handler = logging.FileHandler('sys.log', mode='a', encoding='utf-8')
access_handler.setFormatter(logging.Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
access_logger.addHandler(access_handler)

logger = logging.getLogger('ScanLogger')
logger.setLevel(level=logging.DEBUG)
handler = logging.SysLogHandler(address='/dev/log')
# handler = logging.FileHandler('sys.log', mode='a', encoding='utf-8')
handler.setFormatter(logging.Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(handler)