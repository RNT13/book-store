# Este estágio instala as dependências e prepara o ambiente.
FROM python:3.13.1-slim AS builder

# Configura variáveis de ambiente para Python e Poetry
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VERSION=2.1.4 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false

# Adiciona o Poetry ao PATH do sistema
ENV PATH="$POETRY_HOME/bin:$PATH"

# Instala dependências do sistema necessárias para compilar pacotes Python (como psycopg2)
RUN apt-get update \
    && apt-get install --no-install-recommends -y curl build-essential libpq-dev

# Instala o Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Define o diretório de trabalho e instala as dependências de produção
WORKDIR /app
COPY poetry.lock pyproject.toml ./
# Instala apenas as dependências principais, excluindo as de desenvolvimento (pytest, black, etc. )
RUN poetry install --no-interaction --no-ansi --only main


# ---- Estágio 2: Final ----
# Este estágio cria a imagem final, que é leve e otimizada para produção.
FROM python:3.13.1-slim AS final

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Cria um grupo e um usuário 'app' para rodar a aplicação sem privilégios de root (mais seguro)
RUN addgroup --system app && adduser --system --group app

# Define o diretório de trabalho
WORKDIR /app

# Copia o ambiente virtual com as dependências instaladas do estágio 'builder'
COPY --from=builder /app /app

# Copia o código-fonte da sua aplicação para a imagem
COPY . .

# Define o usuário 'app' como o usuário padrão para executar o comando
USER app

# Expõe a porta que o Gunicorn irá escutar. O Render usará a variável $PORT.
EXPOSE 8000

# O Render injetará a variável de ambiente $PORT automaticamente.
CMD python manage.py migrate && gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
