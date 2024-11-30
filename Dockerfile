FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV MIVILUS_HOST=${MIVILUS_HOST}
ENV MIVILUS_PORT=${MIVILUS_PORT}
ENV MIVILUS_PORT=${MIVILUS_PORT}
ENV POSTGRES_USER=${POSTGRES_USER}
ENV POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
ENV POSTGRES_HOST=${POSTGRES_HOST}
ENV POSTGRES_DB=${POSTGRES_DB}

WORKDIR /

COPY pyproject.toml /
COPY requirements.txt /
COPY /app/domain/ /app/domain
COPY /app/util/ /app/util
COPY /app/repositories /app/repositories
COPY /app/routers /app/routers
COPY /app/services /app/services
COPY app/main.py /app
RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry install

CMD poetry run python -m app.main