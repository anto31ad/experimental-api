import uvicorn

from src import config

if __name__ == "__main__":
    uvicorn.run(
        "src.demo.main:app",
        host=config.DEMO_HOST,
        port=config.DEMO_PORT,
        reload=True  # Remove in production
    )
