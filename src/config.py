from starlette.config import Config

# load environment variables
configDict = Config('.env')

FRONTEND_PROCESS: str = f"http://{configDict.get('FRONTEND_HOST')}:{configDict.get('FRONTEND_PORT')}"

THIS_HOST = configDict.get('THIS_HOST')
THIS_PORT = configDict.get('THIS_PORT')
THIS_PROCESS: str = f"http://{THIS_HOST}:{THIS_PORT}"

ALLOW_ORIGINS = [FRONTEND_PROCESS, THIS_PROCESS]
