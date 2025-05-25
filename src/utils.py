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
