from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
# Здесь также должны быть зарегистрированы ваши прошлые viewsets (categories, manufacturers, и т.д.)

urlpatterns = [
    # Маршруты для HTML-страниц
    path('', views.home_page, name='home'),
    path('catalog/', views.catalog_page, name='catalog'),
    path('product/<int:pk>/', views.product_detail_page, name='product_detail'),
    path('profile/', views.profile_page, name='profile_page'), # Наш личный кабинет
    
    # Маршруты для REST API
    path('api/', include(router.urls)),
    path('api/me/', views.CurrentUserView.as_view(), name='api-me'), # Эндпоинт профиля
]