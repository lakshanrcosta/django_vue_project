FROM python:3.10.4

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY wait-for-it.sh /usr/wait-for-it.sh

RUN chmod +x /usr/wait-for-it.sh

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app