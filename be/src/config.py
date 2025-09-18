from starlette.config import Config

# load environment variables
configDict = Config('.env')

GITHUB_CLIENT_ID = configDict.get('GITHUB_CLIENT_ID')
GITHUB_CLIENT_SECRET = configDict.get("GITHUB_CLIENT_SECRET")

FRONTEND_HOST = configDict.get('FRONTEND_HOST', default='localhost')
FRONTEND_PORT = int(configDict.get('FRONTEND_PORT', default=3000))
FRONTEND_PROCESS: str = f"http://{FRONTEND_HOST}:{FRONTEND_PORT}"

THIS_HOST = configDict.get('THIS_HOST', default='localhost')
THIS_PORT = int(configDict.get('THIS_PORT', default=80))
THIS_PROCESS: str = f"http://{THIS_HOST}:{THIS_PORT}"

GATEWAY_HOST = configDict.get('GATEWAY_HOST', default='localhost')
GATEWAY_PORT = int(configDict.get('GATEWAY_PORT', default=8000))
GATEWAY_PROCESS = f"http://{GATEWAY_HOST}:{GATEWAY_PORT}"

ALLOW_ORIGINS = [
    FRONTEND_PROCESS,
    f"http://localhost:{FRONTEND_PORT}",
    f"http://127.0.0.1:{FRONTEND_PORT}",
    # f"http://192.168.1.208:{FRONTEND_PORT}",
    THIS_PROCESS,
    f"http://localhost:{THIS_PORT}",
    f"http://127.0.0.1:{THIS_PORT}",
    # f"http://192.168.1.208:{THIS_PORT}",
]
