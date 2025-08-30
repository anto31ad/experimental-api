from starlette.config import Config

# load environment variables
configDict = Config('.env')

FRONTEND_HOST = configDict.get('FRONTEND_HOST', default='localhost')
FRONTEND_PORT = int(configDict.get('FRONTEND_PORT', default=3000))
FRONTEND_PROCESS: str = f"http://{FRONTEND_HOST}:{FRONTEND_PORT}"

THIS_HOST = configDict.get('THIS_HOST', default='localhost')
THIS_PORT = int(configDict.get('THIS_PORT', default=8000))
THIS_PROCESS: str = f"http://{THIS_HOST}:{THIS_PORT}"

ALLOW_ORIGINS = [
    FRONTEND_PROCESS,
    # f"http://localhost:{FRONTEND_PORT}",
    f"http://192.168.1.208:{FRONTEND_PORT}",
    THIS_PROCESS,
    # f"http://localhost:{THIS_PORT}",
    # f"http://192.168.1.208:{THIS_PORT}",
]
