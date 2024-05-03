FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8009 8009


WORKDIR /

COPY requirements.txt /
COPY domain/ /
COPY migrations/ /
COPY repositories/ /
COPY routers/ /
COPY services/ /
COPY main.py /
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

CMD python main.py