from typing import Dict

from fastapi import FastAPI, Request
from starlette.responses import JSONResponse, PlainTextResponse

from src.homework.exceptions import raise_specific_status_code_exception
from src.homework.schemas import DivisionInput, KeyValue

app = FastAPI()

memory_storage: dict = {}


@app.middleware('http')
async def check_post_request_content_type(request: Request, call_next):
    if (
        request.method == 'POST'
        and request.headers.get('Content-Type') != 'application/json'
    ):
        return JSONResponse(content={'detail': ''}, status_code=415)
    response = await call_next(request)
    return response


@app.get("/hello", response_class=PlainTextResponse)
def get_hello():
    return "HSE One Love!"


@app.get("/get/{key}", response_model=Dict[str, str])
def get_key_value(key: str):
    if key in memory_storage:
        return {"key": key, "value": memory_storage[key]}
    raise_specific_status_code_exception(status_code=404)
    return None


@app.post("/set")
def set_key_value(kv: KeyValue):
    if kv.key is None or kv.value is None:
        raise_specific_status_code_exception(status_code=400)

    memory_storage[kv.key] = kv.value
    return JSONResponse(content={'detail': ''}, status_code=200)


@app.post("/divide", response_class=PlainTextResponse)
async def divide_numbers(division_input: DivisionInput):
    dividend = division_input.dividend
    divider = division_input.divider

    try:
        result = dividend / divider
    except ZeroDivisionError:
        raise_specific_status_code_exception(status_code=400)
    else:
        return str(result)


@app.api_route("/{path_name:path}")
async def catch_all():
    raise_specific_status_code_exception(status_code=405)
