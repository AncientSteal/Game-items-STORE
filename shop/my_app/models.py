from django.contrib.auth.models import User
from django.db import models

# Создал модель для будущей БД с товарами
class Item(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    available = models.IntegerField()
    image_path = models.CharField(max_length=255, blank=True)

# Создал модель корзины
class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

# Создал модель для товаров в самой корзине
class BasketItem(models.Model):
    basket = models.ForeignKey(Basket, related_name='items', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)