from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='transfer'),
    path('add-transfer', views.add_transfer, name='add-transfer')
]