from django.urls import path
from . import views
urlpatterns = [
    # path('' , views.index),
    path('' , views.index , name="portfolio"),
    path('create/' , views.create, name= 'create_portfolio'),
    path('delete/<int:id>/' , views.delete , name = 'delete_portfolio'),
    path('buy/' , views.buy , name = "buy"),
    path('sell/' , views.sell , name = "sell"),

]

