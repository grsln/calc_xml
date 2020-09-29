from django.urls import path
from .views import index, calc

app_name = 'calc_time'
urlpatterns = [
    path('', index, name='index'),
    path('calc/', calc, name='calc'),
]
