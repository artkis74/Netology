FROM python:3.10.6

WORKDIR /stocks_products

COPY ./stocks_products .

RUN pip install -r /stocks_products/requirements.txt

RUN python /stocks_products/manage.py migrate

CMD gunicorn stocks_products.wsgi -b 0.0.0.0:8000