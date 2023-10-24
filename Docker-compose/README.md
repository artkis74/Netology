
# Docker-compose
## Для запуска проекта необходимо:
Заполнить файл с переменными окружения (.env) в директории stocks_products.   
## Выполнить команду:
```
docker-compose up
```
## Далее необходимо применить миграции:
```
docker-compose exec django_app python manage.py migrate --noinput
```
## Приложение будет доступно:
```
http://localhost:8000/api/v1/
```
