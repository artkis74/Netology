# TODO опишите необходимые обработчики, рекомендуется использовать generics APIView классы:
# TODO ListCreateAPIView, RetrieveUpdateAPIView,
from rest_framework.generics import CreateAPIView, ListCreateAPIView, RetrieveUpdateAPIView

from .models import Sensor
from .serializers import SensorSerializer, SensorInfoSerializer, MeasurementCreateSerializer


class SensorsView(ListCreateAPIView):
    """
       Получить список датчиков методом GET, а также создать новый датчик используя метод POST.
       Список датчиков выводится с краткой информацией по датчикам:
       ID, название и описание.
       Для создания датчика, отправляем json с ключами: 'name' и 'description'
    """
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class SensorInfoView(RetrieveUpdateAPIView):
    """
    Получить информацию по конкретному датчику методом GET со следующей значениями:
    ID, название, описание и список всех измерений с температурой, временем фото(если еть).
    А также обновление информации по конкретному датчику методом PUT и PATCH
    """
    queryset = Sensor.objects.all()
    serializer_class = SensorInfoSerializer


class MeasurementCreate(CreateAPIView):
    """
    Добавить измерение методом POST. Указываются ID датчика и температура в формате json с ключами "sensor" и "temper"
    """
    serializer_class = MeasurementCreateSerializer

