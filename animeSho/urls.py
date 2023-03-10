"""animeSho URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('load/', views.load_db_whoosh, name='load'),
    path('<int:anime_id>/', views.details, name='anime_detail'),
    path('search/', views.custom_search_view, name='search'),
    path('whatchlist/add-remove/<int:anime_id>/', views.add_remove_anime_whatchlist, name='add_remove_anime_whatchlist'),
    path('whatchlist/', views.watchlist, name='whatchlist'),
    path('watchlist/recommendations/', views.recomendations_whatchlist, name='watchlist_recommendations'),
]
