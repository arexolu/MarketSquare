FROM python:3.10-slim-bullseye

EXPOSE 80/tcp

RUN pip install poetry==1.8

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /opt/app

COPY poetry.lock pyproject.toml ./

RUN poetry install --no-root && rm -rf $POETRY_CACHE_DIR

COPY marketsquare marketsquare/

RUN touch README.md
RUN poetry install

CMD ["poetry", "run", "hypercorn", "--bind", "0.0.0.0:80", "marketsquare:app"]