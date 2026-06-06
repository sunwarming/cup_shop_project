from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Product, Category, Manufacturer, Cart, CartItem

# Старые информационные страницы
def home_page(request):
    html_content = """
    <h1>Магазин тематических кружек и термосов</h1>
    <p>Добро пожаловать на главную страницу!</p>
    <ul>
        <li><a href="/catalog/">Каталог товаров (CRUD)</a></li>
        <li><a href="/cart/">Моя корзина</a></li>
        <li><a href="/about-store/">О магазине</a></li>
        <li><a href="/about-author/">Об авторе</a></li>
    </ul>
    """
    return HttpResponse(html_content)

def about_store_page(request):
    text = "Лабораторная работа: Реализация CRUD-операций с Django ORM."
    return HttpResponse(text, content_type="text/plain; charset=utf-8")

def about_author_page(request):
    text = "Выполнил: Студент группы 88ТП Козик Николай"
    return HttpResponse(text, content_type="text/plain; charset=utf-8")


# ================= ЗАДАНИЕ 2: REAL CRUD & ORM =================

# 1. Список товаров (Read)
def product_list(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    manufacturers = Manufacturer.objects.all() # Добавили производителей по ТЗ

    search_query = request.GET.get('search', '')
    if search_query:
        # Используем Q-объекты для поиска по названию ИЛИ описанию
        products = products.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))

    category_id = request.GET.get('category', '')
    if category_id:
        products = products.filter(category_id=category_id)

    manufacturer_id = request.GET.get('manufacturer', '')
    if manufacturer_id:
        products = products.filter(manufacturer_id=manufacturer_id)

    context = {
        'products': products,
        'categories': categories,
        'manufacturers': manufacturers,
        'search_query': search_query,
        'selected_category': category_id,
        'selected_manufacturer': manufacturer_id,
    }
    return render(request, 'shop/product_list.html', context)


# 2. Детальная страница товара (Read)
def product_detail(request, pk):
    # Используем pk (primary key) как указано в задании
    product = get_object_or_404(Product, id=pk)
    return render(request, 'shop/product_detail.html', {'product': product})


# 3. Добавление товара в корзину (Create / Update)
@login_required(login_url='/admin/login/') # Если не залогинен, отправляем на форму в админку
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # Получаем или создаем корзину для текущего юзера
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    # Получаем элемент корзины или создаем новый со стартовым количеством 0
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 0})
    
    # Проверяем, есть ли вообще товар на складе перед добавлением
    if cart_item.quantity + 1 <= product.stock:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('cart_view')


# 4. Просмотр корзины (Read)
@login_required(login_url='/admin/login/')
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    # Благодаря related_name='items' получаем все элементы корзины
    cart_items = cart.items.all() 
    return render(request, 'shop/cart.html', {'cart': cart, 'cart_items': cart_items})


# 5. Обновление количества (Update)
@login_required(login_url='/admin/login/')
def update_cart(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        new_quantity = int(request.POST.get('quantity', 1))
        
        # Валидация: проверяем лимит склада
        if new_quantity <= cart_item.product.stock and new_quantity > 0:
            cart_item.quantity = new_quantity
            cart_item.save()
        elif new_quantity <= 0:
            cart_item.delete() # Если ввели 0, просто удаляем
            
    return redirect('cart_view')


# 6. Удаление товара из корзины (Delete)
@login_required(login_url='/admin/login/')
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart_view')