FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /fastapi_app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./
COPY src ./src
COPY tests ./tests
COPY Makefile .pylintrc ./

RUN poetry config virtualenvs.create false \
    && poetry install

CMD ["uvicorn", "src.homework.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
