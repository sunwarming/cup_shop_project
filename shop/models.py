from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# =====================================================================
# 1. МОДЕЛИ КАТАЛОГА ТОВАРОВ (КРУЖКИ И ТЕРМОСЫ)
# =====================================================================

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    # ИСПРАВЛЕНО: разрешаем сохранять пустые описания категорий
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(max_length=100, verbose_name="Производитель")
    country = models.CharField(max_length=100, verbose_name="Страна")

    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название товара")
    description = models.TextField(verbose_name="Описание товара")
    price = models.DecimalField(max_length=10, max_digits=10, decimal_places=2, verbose_name="Цена (BYN)")
    stock = models.PositiveIntegerField(default=0, verbose_name="Остаток на складе")
    
    # ИСПРАВЛЕНО: upload_to вместо upload_with
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Изображение")
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="Категория")
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name='products', verbose_name="Производитель")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.name


# =====================================================================
# 2. МОДЕЛИ КОРЗИНЫ И ЭЛЕМЕНТОВ КОРЗИНЫ
# =====================================================================

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart', verbose_name="Пользователь")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    @property
    def total_price(self):
        """Вычисляет общую стоимость всех кружек в корзине"""
        return sum(item.item_price for item in self.items.all())

    def __str__(self):
        return f"Корзина пользователя {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name="Корзина")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    class Meta:
        verbose_name = "Элемент корзины"
        verbose_name_plural = "Элементы корзины"

    @property
    def item_price(self):
        """Вычисляет стоимость позиции (цена товара * количество)"""
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} ({self.quantity} шт.)"


# =====================================================================
# 3. МОДЕЛЬ ПРОФИЛЯ ПОЛЬЗОВАТЕЛЯ (ДЛЯ ЛИЧНОГО КАБИНЕТА)
# =====================================================================

class Profile(models.Model):
    # Исправлено на корректный заглавный models.CASCADE
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="Пользователь")
    full_name = models.CharField(max_length=150, blank=True, verbose_name="Полное имя")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Телефон")
    address = models.CharField(max_length=255, blank=True, verbose_name="Адрес")
    
    # Специфичные поля для магазина тематических кружек CupStore
    favorite_mug_type = models.CharField(max_length=100, blank=True, default="Керамическая кружка", verbose_name="Любимый тип кружек")
    delivery_city = models.CharField(max_length=100, blank=True, default="Минск", verbose_name="Город доставки")

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"

    def __str__(self):
        return f"Профиль {self.user.username}"


# =====================================================================
# 4. СИГНАЛЫ ДЛЯ АВТОМАТИЧЕСКОГО СОЗДАНИЯ ПРОФИЛЯ
# =====================================================================

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Создает пустой профиль при регистрации нового User"""
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Сохраняет профиль при обновлении User"""
    instance.profile.save()