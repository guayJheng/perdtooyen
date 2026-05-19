from django.urls import path
from . import views

app_name = 'ingredients'

urlpatterns = [
    path('ingredients/', views.ingredient_search_api, name='search-api'),
]
