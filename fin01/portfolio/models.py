from django.db import models
from user.models import User
# Create your models here.
class Portfolio(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    name = models.CharField(max_length=255 , unique = True, blank = False)
    type = models.CharField(max_length=255 , blank= False)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

class StockPortfolio(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    stock = models.CharField(max_length=255 , null = False, blank=False)
    amount = models.IntegerField(blank=False, null= False)
    def __str__(self) -> str:
        return str(self.portfolio) + " | " + str(self.stock)  + " | " + str(self.amount)