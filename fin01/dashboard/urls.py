from django.urls import path
from . import views
urlpatterns = [
    path('' , views.dashboard , name='dashboard'),
    path('<str:stock>/' , views.get_stock , name ='get_stock'),
]
