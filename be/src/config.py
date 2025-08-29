from starlette.config import Config

# load environment variables
configDict = Config('.env')

FRONTEND_PROCESS: str = f"http://{configDict.get('FRONTEND_HOST')}:{configDict.get('FRONTEND_PORT')}"

THIS_HOST = configDict.get('THIS_HOST', default='localhost')
THIS_PORT = int(configDict.get('THIS_PORT', default=8000))
THIS_PROCESS: str = f"http://{THIS_HOST}:{THIS_PORT}"

ALLOW_ORIGINS = [FRONTEND_PROCESS, THIS_PROCESS]
