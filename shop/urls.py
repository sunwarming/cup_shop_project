from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('about-store/', views.about_store_page, name='about_store'),
    path('about-author/', views.about_author_page, name='about_author'),
]