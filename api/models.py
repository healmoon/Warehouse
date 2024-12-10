from django.contrib.auth.models import AbstractUser
from django.db import models

"""модель пользователя"""
class ApiUser(AbstractUser):

    USER_TYPE_CHOICES = (
        ('supplier', 'Поставщик'),
        ('consumer', 'Потребитель'),
    )
    user_type = models.CharField(max_length=50, choices=USER_TYPE_CHOICES)


"""модель склада"""
class Warehouse(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


"""модель продукта"""
class Product(models.Model):
    count = models.PositiveIntegerField()
    name = models.CharField(max_length=100)
    warehouse = models.ForeignKey(Warehouse, related_name="products", on_delete=models.CASCADE)

