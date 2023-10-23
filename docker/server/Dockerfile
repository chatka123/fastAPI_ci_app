FROM python:3.11 AS builder

WORKDIR /fastapi_app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --no-dev

FROM python:3.11-slim

WORKDIR /fastapi_app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY src ./src

CMD ["uvicorn", "src.homework.main:app", "--host", "0.0.0.0", "--port", "8000"]
