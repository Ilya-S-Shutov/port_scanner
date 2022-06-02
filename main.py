from aiohttp import web
import socket
import json
import time
from typing import Dict, Union
from logger_settings import access_logger, logger
from exceptions import NumPortError, BeginMoreThenEndError, IpError


routes = web.RouteTableDef()


def valid_ip(ip: str) -> bool:
    """
    valid_ip определяет валидность IP-адреса.

    Пытается преобазовать в двоичный код. При неверном формате возвращает OSError.
    """
    try: 
        socket.inet_aton(ip)
        return True
    except:
        return False


def scan_port(ip: str, port: int) -> Dict[str, Union[int, str]]:
    """
    scan_port сканирует указанный порт хоста.

    Функция пытается установить соединение  с портом хоста. Если соединение успешно —
    это открытый TCP-порт, иначе — порт закрыт.

    Args:
        ip (str): IP-адресс хоста.
        port (int): сканируемый порт.

    Returns:
        Dict[str, Union[int, str]]: словарь, содержащий номер и состояние сканируемого порта.
    """
    port_info: dict = dict()
    port_info['Port'] = port

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.01)

    try:
        sock.connect((ip, port))
        port_info['state'] = 'open'

    
    except socket.timeout:
        port_info['state'] = 'closed'

    finally:
        sock.close()
        return port_info



@routes.get('/scan/{ip}/{begin_port}/{end_port}')
async def scanner(request) -> web.json_response:
    """
    scanner обработчик клиентских GET запросов.

    Args:
        request (aiohttp.web_request.Request): обрабатываемый запрос. Содержит IP-адресс, номера начального 
        и конечного портов диапазона для сканирования.

    Raises:
        BeginMoreThenEndError: номер последнего порта больше, чем номер начального.
        NumPortError: указанный номер порта begin_port ошибочен.
        NumPortError: указанный номер порта end_port ошибочен.
        IpError: IP-адрес имеет неверный формат.

    Returns:
        web.json_response: список словарей, содержащих информацию о портах в формате json.
    """
    # print(type(request))
    port_list = []
    start = time.time()

    try:
        begin_port: int = int(request.match_info['begin_port'])
        end_port: int = int(request.match_info['end_port'])
        ip: str = request.match_info['ip']

        if begin_port > end_port:
            raise BeginMoreThenEndError
        if not 0 < begin_port <=65535:
            raise NumPortError('begin_port')
        if not 0 < end_port <=65535:
            raise NumPortError('end_port')
        if not valid_ip(ip):
            raise IpError

        for port in range(begin_port, end_port + 1):
            port_list.append(scan_port(ip, port))
    
    except ValueError as err:
        logger.exception('Port numbers must not contain letters', exc_info=err)
        return web.json_response('Port numbers must not contain letters!', status=400)

    except (NumPortError, BeginMoreThenEndError, IpError) as err:
        logger.exception(str(err), exc_info=err)
        return web.json_response(str(err), status=400)

    except Exception as err:
        logger.exception(str(err), exc_info=err)
        return web.json_response('Unexpected error!', status=400)

    else:
        # data = json.dumps(port_list, indent=4)
        return web.json_response(port_list, status=200)
    
    finally:
        res_time = time.time() - start
        logger.debug(f'Request processing time: {res_time}')


if __name__ == '__main__':

    app = web.Application()
    app.add_routes(routes)
    web.run_app(
                app, 
                port=8000, 
                access_log_format='"%r" %s %b "%{Referer}i" "%{User-Agent}i"'
                )
