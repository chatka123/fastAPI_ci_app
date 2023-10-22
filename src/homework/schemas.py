from pydantic import BaseModel


class KeyValue(BaseModel):
    key: str | None = None
    value: str | None = None


class DivisionInput(BaseModel):
    dividend: int
    divider: int
