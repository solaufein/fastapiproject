## How to install
    .\venv\Scripts\activate
    pip install -r requirements.txt

## How to run app
    uvicorn fastapiproject.core.application:app --reload
    or 
    pycharm run main.py

## How to run API
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/fastapi/healthcheck
- http://127.0.0.1:8000/fastapi/users/{user_id}
- http://127.0.0.1:8000/fastapi/error-http
- http://127.0.0.1:8000/fastapi/error-generic