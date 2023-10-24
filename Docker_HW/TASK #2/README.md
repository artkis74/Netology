Создание образа
=======================
docker build . --tag=drf

Создание контейнера
======================
docker run --name=docker_hw -d -p 8001:8000 drf
