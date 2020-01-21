from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from starlette.status import HTTP_201_CREATED, HTTP_200_OK
from starlette.responses import JSONResponse

import settings

from ..service import KV


router = APIRouter()
kv = KV(**settings.KV_CONFIG)


class Item(BaseModel):
    key: str
    value: dict


class PutItem(BaseModel):
    value: dict


class ExceptionResponse(BaseModel):
    status_code: int
    detail: Any
    headers: dict

class Response(BaseModel):
    message: Any


@router.post(
    "",
    status_code=HTTP_201_CREATED,
    response_description="Item is created",
    responses={
        404: {"model": ExceptionResponse, "description": "Item with such key already exists"},
        400: {"content": {"application/json": {"schema": {"$ref": "#/components/schemas/HTTPValidationError"}}}}
    })
def post(item: Item):
    try:
        kv.put(item.key, item.value)
    except KeyError as err:
        return HTTPException(409, detail=str(err))
    return item


@router.get(
    "/{key:str}",
    response_description="Item is received",
    responses={
        404: {"description": "Item with such key was not found"}
    }
)
def get(key: str):
    try:
        ret = kv.get(key)
    except KeyError as err:
        return HTTPException(404, detail=str(err))
    else:
        return ret


@router.put(
    "/{key:str}",
    status_code=HTTP_200_OK,
    response_description="Item is updated",
    responses={
        404: {"model": ExceptionResponse, "description": "Item with such key was not found"},
        400: {"content": {"application/json": {"schema": {"$ref": "#/components/schemas/HTTPValidationError"}}}}
    }
)
def put(key: str, updater: PutItem):
    try:
        ret = kv.update(key, updater.value)
    except KeyError as err:
        return HTTPException(400, str(err))
    else:
        return Item(key=key, value=ret)


@router.delete(
    "/{key:str}",
    response_description="Item is removed",
    responses={
        404: {"model": ExceptionResponse, "description": "Item with such key was not found"}
    }
)
def put(key: str):
    try:
        ret = kv.delete(key)
    except KeyError as err:
        return HTTPException(400, str(err))
    else:
        return Item(key=key, value=ret)
