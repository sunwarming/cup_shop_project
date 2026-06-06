document.addEventListener('DOMContentLoaded', function() {
    // Элементы страницы каталога
    const productsGrid = document.getElementById('products-grid');
    const loadingSpinner = document.getElementById('loading-spinner');
    const errorMessage = document.getElementById('error-message');
    const filterForm = document.getElementById('filter-form');

    // Проверяем, находимся ли мы на странице каталога, где есть сетка
    if (productsGrid) {
        // Первичная загрузка всех товаров
        fetchProducts();

        // Обработка отправки формы фильтров
        filterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const search = document.getElementById('search-input').value;
            const category = document.getElementById('category-select').value;
            const manufacturer = document.getElementById('manufacturer-select').value;

            // Строим строку параметров запроса для API
            let urlParams = new URLSearchParams();
            if (search) urlParams.append('search', search);
            if (category) urlParams.append('category', category);
            if (manufacturer) urlParams.append('manufacturer', manufacturer);

            fetchProducts(urlParams.toString());
        });
    }

    // --- ФУНКЦИЯ ЗАГРУЗКИ ТОВАРОВ ИЗ REST API (GET) ---
    function fetchProducts(queryString = '') {
        // Показываем спиннер, чистим сетку и скрываем старые ошибки
        loadingSpinner.classList.remove('d-none');
        productsGrid.innerHTML = '';
        errorMessage.classList.add('d-none');

        let url = '/api/products/';
        if (queryString) {
            url += `?${queryString}`;
        }

        fetch(url)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Сетевая ошибка при получении данных от API ресурса.');
                }
                return response.json();
            })
            .then(data => {
                loadingSpinner.classList.add('d-none');
                
                // В зависимости от настроек пагинации DRF, данные могут быть в массиве напрямую или в ключе 'results'
                const products = Array.isArray(data) ? data : data.results;

                if (products.length === 0) {
                    productsGrid.innerHTML = `
                        <div class="col-12 text-center my-5">
                            <i class="bi bi-search" style="font-size: 3rem; color: #ccc;"></i>
                            <p class="mt-2 text-muted">Кружки с такими параметрами не найдены. Попробуйте изменить фильтры!</p>
                        </div>`;
                    return;
                }

                // Динамическое построение Bootstrap-карточек
                products.forEach(product => {
                    const cardHtml = `
                        <div class="col">
                            <div class="card h-100 shadow-sm card-product">
                                <div class="bg-light text-center py-4 text-secondary border-bottom position-relative" style="height: 200px; overflow:hidden;">
                                    <i class="bi bi-cup-hot position-absolute top-50 start-50 translate-middle" style="font-size: 4rem; opacity: 0.1;"></i>
                                    <span class="badge bg-dark position-absolute top-2 start-2">${product.category_name || 'Кружка'}</span>
                                </div>
                                <div class="card-body d-flex flex-column">
                                    <h5 class="card-title fw-bold text-dark">${product.name}</h5>
                                    <p class="card-text text-muted flex-grow-1 small">${product.description || 'Без описания'}</p>
                                    <div class="mt-3">
                                        <div class="d-flex justify-content-between align-items-center mb-2">
                                            <span class="fs-5 fw-bold text-success">${product.price} BYN</span>
                                            <span class="small text-muted">Запас: ${product.stock} шт.</span>
                                        </div>
                                        <div class="row g-2">
                                            <div class="col-6">
                                                <a href="/product/${product.id}/" class="btn btn-outline-dark btn-sm w-100">Инфо</a>
                                            </div>
                                            <div class="col-6">
                                                <button class="btn btn-warning btn-sm w-100 fw-bold btn-add-to-cart" 
                                                        data-id="${product.id}" 
                                                        ${product.stock <= 0 ? 'disabled' : ''}>
                                                    ${product.stock <= 0 ? 'Нет' : '<i class="bi bi-cart-plus"></i>'}
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                    productsGrid.insertAdjacentHTML('beforeend', cardHtml);
                });

                // Вешаем слушатели кликов на свежесозданные кнопки "В корзину"
                initCartButtons();
            })
            .catch(error => {
                loadingSpinner.classList.add('d-none');
                errorMessage.textContent = `Ошибка: ${error.message}. Не удалось загрузить каталог товаров.`;
                errorMessage.classList.remove('d-none');
            });
    }

    // Инициализация кнопок добавления в корзину
    function initCartButtons() {
        const buttons = document.querySelectorAll('.btn-add-to-cart');
        buttons.forEach(button => {
            button.addEventListener('click', function() {
                const productId = this.getAttribute('data-id');
                addToCartAPI(productId);
            });
        });
    }

    // --- ФУНКЦИЯ ДОБАВЛЕНИЯ В КОРЗИНУ ЧЕРЕЗ REST API (POST) ---
    function addToCartAPI(productId) {
        // Мы отправляем запись в эндпоинт элементов корзины
        // По умолчанию DRF ожидает ID корзины, ID товара и количество.
        // Передаем CSRF-токен в заголовках, чтобы Django пропустил запрос
        fetch('/api/cart-items/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({
                cart: 1, // В реальном проекте ID корзины юзера подтягивается динамически или обрабатывается бэкендом
                product: parseInt(productId),
                quantity: 1
            })
        })
        .then(response => {
            if (response.status === 403 || response.status === 401) {
                showNotification('Внимание', 'Пожалуйста, авторизуйтесь для добавления товаров в корзину!', 'danger');
                return;
            }
            if (!response.ok) {
                throw new Error('Ошибка добавления. Проверьте остатки товара.');
            }
            return response.json();
        })
        .then(data => {
            if (data) {
                showNotification('Успех!', 'Кружка успешно добавлена в вашу корзину!', 'success');
            }
        })
        .catch(error => {
            showNotification('Ошибка', error.message, 'danger');
        });
    }

    // --- ФУНКЦИЯ ПОКАЗА УВЕДОМЛЕНИЙ (Bootstrap Alerts) ---
    function showNotification(title, message, type = 'success') {
        const alertContainer = document.getElementById('alert-container');
        if (!alertContainer) return;

        const alertId = 'alert_' + Date.now();
        const alertHtml = `
            <div id="${alertId}" class="alert alert-${type} alert-dismissible fade show shadow-sm" role="alert">
                <strong>${title}</strong> ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>
        `;
        
        alertContainer.insertAdjacentHTML('beforeend', alertHtml);

        // Автоматическое удаление уведомления через 4 секунды
        setTimeout(() => {
            const currentAlert = document.getElementById(alertId);
            if (currentAlert) {
                const bsAlert = new bootstrap.Alert(currentAlert);
                bsAlert.close();
            }
        }, 4000);
    }
});