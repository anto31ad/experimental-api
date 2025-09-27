import uvicorn

from src import main

if __name__ == "__main__":
    print(f"{main.SERVICE_HOST}:{main.SERVICE_PORT}")
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=main.SERVICE_PORT,
        reload=True  # Remove in production
    )
