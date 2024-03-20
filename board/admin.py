from django.contrib import admin
from .models import Product, Order


class ProductAdmin(admin.ModelAdmin):
    # list_display — это список или кортеж со всеми полями, которые вы хотите видеть в таблице с товарами
    # list_display = [field.name for field in
    #                 Product._meta.get_fields()]  # генерируем список имён всех полей для более красивого отображения
    list_display = ('name', 'price') # оставляем только имя и цену товара и свойства

admin.site.register(Product)
admin.site.register(Order)
# admin.site.unregister(Product) # разрегистрируем наши товары