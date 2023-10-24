FROM python:3.10.6

WORKDIR /stocks_products

COPY ./stocks_products .

RUN pip install -r /stocks_products/requirements.txt
ENV USER admin1
ENV PASSWORD admin1pwd

CMD gunicorn stocks_products.wsgi -b 0.0.0.0:8000