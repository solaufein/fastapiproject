"""Application module."""

import logging
from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from fastapiproject.api import endpoints
from fastapiproject.core.containers import Container


class RequestIdHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid4())

        try:
            response = await call_next(request)
        except Exception as exc:
            return exception_handler(request, exc)

        response.headers["X-Request-Id"] = request_id
        return response


def exception_handler(request: Request, exc: Exception):
    logging.error(f"Exception occurred: {exc}")

    return JSONResponse({"detail": str(exc)}, status_code=400)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info(f"Startup...")
    c = app.container
    c.init_resources()
    db = c.db()
    db.create_database()
    yield
    logging.info(f"Shutdown...")
    c.shutdown_resources()


def create_app() -> FastAPI:
    container = Container()

    app = FastAPI(lifespan=lifespan)
    app.container = container
    app.include_router(endpoints.router)
    app.add_middleware(RequestIdHeaderMiddleware)
    app.add_exception_handler(HTTPException, exception_handler)
    app.add_exception_handler(Exception, exception_handler)
    return app


app = create_app()
