# `python-base` sets up all our shared environment variables
FROM python:3.13.1-slim AS python-base

# python / pip / poetry configs
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=2.1.4 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# system deps
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential

# install poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# postgresql dependencies
RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

# install python deps
WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./
RUN poetry install --no-root --with dev

# copy project
WORKDIR /app
COPY . .

# expose port
EXPOSE 8000

# ✅ RUN GUNICORN USING PORT FROM RENDER
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:${PORT}"]
