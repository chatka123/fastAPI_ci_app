from fastapi import HTTPException


def raise_specific_status_code_exception(status_code: int):
    raise HTTPException(status_code=status_code, detail='')