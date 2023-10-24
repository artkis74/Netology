from django.urls import path

from .views import SensorsView, SensorInfoView, MeasurementCreate

urlpatterns = [
    path('sensors/', SensorsView.as_view()),
    path('sensors/<pk>/', SensorInfoView.as_view()),
    path('measurement/', MeasurementCreate.as_view())
]
