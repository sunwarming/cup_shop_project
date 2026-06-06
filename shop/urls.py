from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('about-store/', views.about_store_page, name='about_store'),
    path('about-author/', views.about_author_page, name='about_author'),
    
    # Каталог товаров
    path('catalog/', views.product_list, name='product_list'),
    path('catalog/<int:pk>/', views.product_detail, name='product_detail'),
    
    # Операции с корзиной (CRUD)
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
]