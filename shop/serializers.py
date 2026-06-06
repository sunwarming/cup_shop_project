from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, Category, Manufacturer, Cart, CartItem, Profile

# =====================================================================
# 1. СЕРИАЛИЗАТОРЫ ПРОФИЛЯ И ПОЛЬЗОВАТЕЛЯ
# =====================================================================

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['full_name', 'phone', 'address', 'favorite_mug_type', 'delivery_city']


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    is_admin = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile', 'is_admin']

    def get_is_admin(self, obj):
        return obj.is_staff or obj.is_superuser

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        
        # Обновляем email самого пользователя
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        
        # Обновляем вложенные данные кастомного профиля
        profile = instance.profile
        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        profile.save()
        
        return instance


# =====================================================================
# 2. СЕРИАЛИЗАТОРЫ КАТАЛОГА ТОВАРОВ
# =====================================================================

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    # Показываем названия текстом в API для удобства фронтенда
    category_name = serializers.ReadOnlyField(source='category.name')
    manufacturer_name = serializers.ReadOnlyField(source='manufacturer.name')

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'stock', 
            'image', 'category', 'category_name', 'manufacturer', 'manufacturer_name'
        ]


# =====================================================================
# 3. СЕРИАЛИЗАТОРЫ КОРЗИНЫ
# =====================================================================

class CartItemSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)
    item_price = serializers.ReadOnlyField()

    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product', 'product_details', 'quantity', 'item_price']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'items', 'total_price']