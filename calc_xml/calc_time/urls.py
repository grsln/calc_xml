from django.urls import path
from .views import index, calc, after_upload

app_name = 'calc_time'
urlpatterns = [
    path('', index, name='index'),
    path('upload/', after_upload, name='after_upload'),
    path('calc/', calc, name='calc'),
]
