
# Final_work
## Для запуска проекта необходимо:
Заполнить файл с переменными окружения (.env)
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
