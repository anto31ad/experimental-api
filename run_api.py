import uvicorn

from src import config

if __name__ == "__main__":
    uvicorn.run(
        "src.api.main:app",
        host=config.THIS_HOST,
        port=int(config.THIS_PORT),
        reload=True  # Remove in production
    )
