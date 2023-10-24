FROM python:3.10.6

COPY requirements.txt /temp/requirements.txt
COPY shop /shop
WORKDIR /shop
EXPOSE 8000

ENV PATH_TO_ENV .env
RUN export $(cat $PATH_TO_ENV | xargs)

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password shop-user

USER shop-user