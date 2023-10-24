from django.urls import path
from . import views
urlpatterns = [
    # path('' , views.index),
    path('register/', views.register , name='user_register'),
    path('login/', views.login, name='user_login'),
    path('logout/' , views.logout_view , name='user_logout'),
    path('', views.get_user_info, name= 'user_info'),
    path('reset_password/' , views.reset_password , name='reset_password'),
    path('deposit/', views.deposit, name ="deposit"),
]

