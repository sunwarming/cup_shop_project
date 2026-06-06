from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User  # Импортируем встроенную модель User
from decimal import Decimal

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Категория товара"
        verbose_name_plural = "Категории товаров"

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название производителя")
    country = models.CharField(max_length=100, verbose_name="Страна")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название товара")
    description = models.TextField(verbose_name="Подробное описание")
    image = models.ImageField(upload_to='products/', verbose_name="Фото товара", blank=True, null=True)
    
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name="Цена"
    )
    
    stock = models.IntegerField(
        validators=[MinValueValidator(0)],
        verbose_name="Количество на складе"
    )
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, verbose_name="Производитель")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name


# ================= ЗАДАНИЕ 2 =================

class Cart(models.Model):
    # Связь один-к-одному: у одного юзера может быть только одна корзина
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f"Корзина пользователя {self.user.username}"

    # Метод для подсчета общей стоимости всей корзины
    @property
    def total_price(self):
        # Суммируем стоимость каждого элемента в этой корзине
        return sum(item.item_price for item in self.items.all())


class CartItem(models.Model):
    # Related_name='items' позволяет нам легко получать элементы из объекта корзины (как в методе выше)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name="Корзина")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(verbose_name="Количество")

    class Meta:
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Элементы корзины"

    def __str__(self):
        return f"{self.product.name} ({self.quantity} шт.)"

    # Метод стоимости конкретной позиции (цена товара * количество)
    @property
    def item_price(self):
        return self.product.price * self.quantity

    # Валидация: количество не должно превышать остаток на складе
    def clean(self):
        if self.product and self.quantity > self.product.stock:
            raise ValidationError(
                f"Невозможно добавить {self.quantity} шт. На складе доступно только {self.product.stock} шт."
            )

    def save(self, *args, **kwargs):
        self.full_clean() # Принудительно вызываем валидацию перед сохранением в админке
        super().save(*args, **kwargs)