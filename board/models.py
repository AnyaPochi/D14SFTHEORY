from django.db import models
from django.shortcuts import reverse
from django.core.validators import MinValueValidator
from django.core.cache import cache
class Product(models.Model):
    name = models.CharField(max_length = 255)
    price = models.FloatField(default = 0.0)
    quantity = models.IntegerField(validators=[MinValueValidator(0, 'Quantity should be >= 0')])
    category = models.ForeignKey('Category', on_delete=models.CASCADE)

    # допишем свойство, которое будет отображать, есть ли товар на складе
    @property
    def on_stock(self):
        return self.quantity > 0

    def __str__(self):
        return f'{self.name} {self.quantity}'

    def get_absolute_url(self):  # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с товаром
        return f'/products/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'product-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его


    def __str__(self):
        return self.name + "/" + str(self.price)


# модель категории
class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name}'

class Order(models.Model):
    time_in = models.DateTimeField(auto_now_add = True)
    time_out = models.DateTimeField(null = True)
    cost = models.FloatField(default = 0.0)
    take_away = models.BooleanField(default = False)
    complete = models.BooleanField(default = False)
    
    products = models.ManyToManyField(Product, through = 'ProductOrder')

class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE, related_name = 'products_in')
    order = models.ForeignKey(Order, on_delete = models.CASCADE)
    amount = models.IntegerField(default = 1) 