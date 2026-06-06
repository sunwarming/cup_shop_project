from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Создаем роутер для API и регистрируем ViewSets
router = DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='api-product')
router.register(r'categories', views.CategoryViewSet, basename='api-category')
router.register(r'manufacturers', views.ManufacturerViewSet, basename='api-manufacturer')
router.register(r'carts', views.CartViewSet, basename='api-cart')
router.register(r'cart-items', views.CartItemViewSet, basename='api-cartitem')

urlpatterns = [
    # Старые HTML-маршруты магазина (ИСПРАВЛЕНО: везде теперь двоеточие ":")
    path('', views.home_page, name='home'),
    path('about-store/', views.about_store_page, name='about_store'),
    path('about-author/', views.about_author_page, name='about_author'),
    path('catalog/', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),

    # Включаем все сгенерированные роутером API маршруты по префиксу api/
    path('api/', include(router.urls)),
]