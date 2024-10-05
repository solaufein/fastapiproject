## How to install
    .\venv\Scripts\activate
    pip install -r requirements.txt

## How to run app
    uvicorn fastapiproject.application:app --reload

## How to run API
- http://127.0.0.1:8000/error-http
- http://127.0.0.1:8000/error-generic
- http://127.0.0.1:8000/users/{user_id}
- http://127.0.0.1:8000/healthcheck