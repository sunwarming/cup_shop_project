from django.http import HttpResponse

def home_page(request):
    # Главная страница со ссылками на две другие
    html_content = """
    <h1>Магазин тематических кружек и термосов</h1>
    <p>Добро пожаловать на главную страницу!</p>
    <ul>
        <li><a href="/about-store/">О магазине</a></li>
        <li><a href="/about-author/">Об авторе</a></li>
    </ul>
    """
    return HttpResponse(html_content)

def about_store_page(request):
    text = (
        "Тема лабораторной работы: Разработка интернет-магазина тематических кружек и термосов.\n"
        "Здесь вы найдете кружки с принтами из любимых игр, сериалов и аниме, а также надежные "
        "термосы для долгих прогулок и путешествий."
    )
    return HttpResponse(text, content_type="text/plain; charset=utf-8")

def about_author_page(request):
    text = (
        "Лабораторную работу выполнил:\n"
        "Учащийся группы 88ТП\n"
        "Козик Николай"
    )
    return HttpResponse(text, content_type="text/plain; charset=utf-8")