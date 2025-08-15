import socket
from urllib.parse import urlparse

def validate_url(url: str, allowed_origins: list[str]) -> bool:

    parsedRes = urlparse(url)

    if not parsedRes.path:
        return False
    elif parsedRes.path.startswith('/'):
        return True
    elif any(parsedRes.path.startswith(prefix) \
        for prefix in allowed_origins):
        return True
    
    return False

def is_same_process(
    hostname_a: str = '',
    port_a: int = 0,
    hostname_b: str = '',
    port_b: int = 0
) -> bool:

    addr_a = socket.gethostbyname(hostname_a) 
    addr_b = socket.gethostbyname(hostname_b) 

    same_host = addr_a == addr_b 
    same_port = int(port_a) == int(port_b)

    return same_host and same_port
