from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from .routes import kv


app = FastAPI(openapi_prefix="/api")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}), status_code=400)


def rm422s():
    openapi = app.openapi()
    for v in openapi["paths"].values():
        for meth in v.values():
            resps = meth["responses"]
            if "422" in resps:
                del resps["422"]


app.include_router(
    kv.router,
    prefix="/kv",
    tags=["kv"],
)

rm422s()
