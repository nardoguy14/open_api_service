FROM python:3.12

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

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
#    && pip install -r requirements.txt

CMD poetry shell && python -m app.main