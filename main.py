# Run locally with PyCharm
import uvicorn

if __name__ == '__main__':
    uvicorn.run("fastapiproject.core.application:app", host="127.0.0.1", port=8000, reload=True)