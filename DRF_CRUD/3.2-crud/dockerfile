FROMROM python:3.10
WORKDIR ./stocks_products
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000
RUN python manage.py migrate
CMD gunicorn my_proj.wsgi -b 0.0.0.0:8000