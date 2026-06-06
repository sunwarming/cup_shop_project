from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Product, Category, Manufacturer
from .serializers import ProductSerializer, UserSerializer
from .permissions import IsAdminOrReadOnly

# =====================================================================
# 1. СТАНДАРТНЫЕ ПРЕДСТАВЛЕНИЯ (HTML-СТРАНИЦЫ)
# =====================================================================

def home_page(request):
    """Главная страница магазина"""
    return render(request, 'shop/index.html')

def catalog_page(request):
    """Страница каталога товаров"""
    return render(request, 'shop/catalog.html')

def product_detail_page(request, pk):
    """Страница детальной информации о кружке"""
    return render(request, 'shop/product_detail.html', {'pk': pk})

def profile_page(request):
    """Страница Личного кабинета пользователя"""
    return render(request, 'shop/profile.html')


# =====================================================================
# 2. REST API ПРЕДСТАВЛЕНИЯ (DJANGO REST FRAMEWORK)
# =====================================================================

class ProductViewSet(viewsets.ModelViewSet):
    """
    API для работы с товарами.
    Просмотр доступен всем, редактирование — только администраторам.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        queryset = Product.objects.all()
        category_id = self.request.query_params.get('category')
        manufacturer_id = self.request.query_params.get('manufacturer')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if manufacturer_id:
            queryset = queryset.filter(manufacturer_id=manufacturer_id)
        return queryset


class CurrentUserView(APIView):
    """
    API-эндпоинт (/api/me/), возвращающий или обновляющий 
    профиль текущего аутентифицированного пользователя.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Возвращает данные профиля"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        """Частично обновляет данные профиля (Fetch PATCH)"""
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)