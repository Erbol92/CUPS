from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class CupSize(models.Model):
    name = models.CharField(verbose_name='размер', max_length=10)

    def __str__(self):
        return self.name.upper()
    
    class Meta:
        verbose_name = 'размер'
        verbose_name_plural = 'размеры'

class CupGroup(models.Model):
    name = models.CharField('наименование группы', max_length=50)

    def __str__(self):
        return self.name.upper()
    
    class Meta:
        verbose_name = 'тип'
        verbose_name_plural = 'типы'

class Product(models.Model):
    group = models.ForeignKey(CupGroup, verbose_name='группа', on_delete=models.CASCADE, related_name='group_products')
    size = models.ForeignKey(CupSize, verbose_name='размер', on_delete=models.CASCADE, related_name='size_products', blank=True, null=True)
    name = models.CharField('название', max_length=50)
    description = models.TextField('описание')
    price = models.PositiveIntegerField(verbose_name='цена за ед', default=300)


    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        ordering = ['group','name']

class Order(models.Model):
    product = models.ForeignKey(Product, verbose_name='товар', on_delete=models.DO_NOTHING)
    quantity = models.IntegerField('кол-во',default=1)
    created_at = models.DateTimeField('время заказа',auto_now=True)
    user = models.ForeignKey(User, verbose_name='пользователь',on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'{self.product.name} {self.product.price} {self.quantity}'
    
    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'
        ordering = ['-created_at']