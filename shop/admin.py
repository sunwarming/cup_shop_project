from django.contrib import admin
from .models import Category, Manufacturer, Product, Cart, CartItem

# Позволяет редактировать элементы корзины прямо внутри страницы самой корзины
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1 # Сколько пустых строк для новых товаров отображать по умолчанию

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'country')
    list_display_links = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'stock', 'category', 'manufacturer')
    list_display_links = ('name',)
    list_filter = ('category', 'manufacturer')
    search_fields = ('name', 'description')

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at', 'get_total_price')
    inlines = [CartItemInline] # Подключаем элементы корзины

    # Отображаем нашу кастомную общую стоимость в общем списке админки
    def get_total_price(self, obj):
        return obj.total_price
    get_total_price.short_description = "Общая стоимость"