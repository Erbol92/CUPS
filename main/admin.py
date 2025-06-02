from django.contrib import admin
from .models import CupGroup,CupSize,Product, Order
# Register your models here.
@admin.register(CupGroup)
class CupGroupAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(CupSize)
class CupSizeAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'size', 'group', 'price']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['product','product__size','product__price', 'quantity', 'created_at']
    list_filter = ['user', 'created_at']
    def product__size(self, obj):
        return obj.product.size.name if obj.product.size else 'Нет размера'
    product__size.short_description = 'Размер'

    def product__price(self, obj):
        return obj.product.price if obj.product.price else 'Нет цены'
    product__price.short_description = 'Размер'
        