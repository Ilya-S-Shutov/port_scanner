"""Подключаемый модуль, содержащий дополнительные классы исключений."""


class NumPortError(Exception):
    """
    NumPortError вызывается, если указанный номер порта ошибочен.
    """
    def __init__(self, port: str, message: str='{} cannot be higher then 65535 and lower then 0!') -> None:
        self.message = message.format(port)
        super().__init__(self.message)
    

class BeginMoreThenEndError(Exception):
    """
    BeginMoreThenEndError вызывается, если номер последнего порта больше, чем номер начального.

    Args:
        Exception (_type_): _description_
    """
    def __init__(self, message: str='End_port must be higher then begin_port!') -> None:
        self.message = message
        super().__init__(message)


class IpError(Exception):
    """
    NumPortError вызывается, если указанный IP-адрес имеет неверный формат.
    """
    def __init__(self, message: str='Invalid IP address format!')-> None:
        self.message = message
        super().__init__(message)