from typing import Any, Union

from fastapi import APIRouter
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


class Message(BaseModel):
    message: Union[Item, dict, str]


@router.post(
    "",
    status_code=HTTP_201_CREATED,
    response_description="Item is created",
    responses={
        409: {"model": Message, "description": "Item with such key already exists"},
        400: {"content": {"application/json": {"schema": {"$ref": "#/components/schemas/HTTPValidationError"}}}}
    })
def post(item: Item):
    try:
        kv.put(item.key, item.value)
    except KeyError as err:
        return JSONResponse(status_code=409, content={"message": str(err)})
    return item


@router.get(
    "/{key:str}",
    response_model=Message,
    response_description="Item is received",
    responses={
        404: {"model": Message, "description": "Item with such key was not found"}
    }
)
def get(key: str):
    try:
        ret = kv.get(key)
    except KeyError as err:
        return JSONResponse(status_code=404, content={"message": str(err)})
    else:
        return {"message": ret}


@router.put(
    "/{key:str}",
    status_code=HTTP_200_OK,
    response_model=Message,
    response_description="Item is updated",
    responses={
        404: {"model": Message, "description": "Item with such key was not found"},
        400: {"content": {"application/json": {"schema": {"$ref": "#/components/schemas/HTTPValidationError"}}}}
    }
)
def put(key: str, updater: PutItem):
    try:
        ret = kv.update(key, updater.value)
    except KeyError as err:
        return JSONResponse(status_code=404, content={"message": str(err)})
    else:
        return {"message": dict(key=key, value=ret)}


@router.delete(
    "/{key:str}",
    response_description="Item is removed",
    responses={
        404: {"model": Message, "description": "Item with such key was not found"}
    }
)
def put(key: str):
    try:
        ret = kv.delete(key)
    except KeyError as err:
        return JSONResponse(status_code=404, content={"message": str(err)})
    else:
        return {"message": dict(key=key, value=ret)}
