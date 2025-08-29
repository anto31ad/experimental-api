import uvicorn

from be import main

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=main.SERVICE_PORT,
        reload=True  # Remove in production
    )
