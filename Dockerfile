FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /

COPY requirements.txt /
COPY /domain/ /domain
COPY /repositories /repositories
COPY /routers /routers
COPY /services /services
COPY main.py /
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

CMD python main.py