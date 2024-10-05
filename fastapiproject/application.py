"""Application module."""

import logging

import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from fastapiproject import endpoints
from fastapiproject.containers import Container


class HeaderAddingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            # Attempt to get a response from the route or next middleware
            response = await call_next(request)
        except Exception as exc:
            return exception_handler(request, exc)

        # Add the custom header to every response
        response.headers["X-Custom-Header"] = "Custom Value"
        return response


def exception_handler(request: Request, exc: Exception):
    logging.error(f"Exception occurred: {exc}")

    return JSONResponse({"detail": str(exc)}, status_code=400)


def create_app() -> FastAPI:
    container = Container()
    container.init_resources()

    app = FastAPI()
    app.container = container
    app.include_router(endpoints.router)
    app.add_middleware(HeaderAddingMiddleware)
    app.add_exception_handler(HTTPException, exception_handler)
    app.add_exception_handler(Exception, exception_handler)
    return app


app = create_app()

# Run locally with PyCharm
if __name__ == '__main__':
    uvicorn.run("application:app", host="127.0.0.1", port=8000, reload=True)
