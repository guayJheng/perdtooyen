from django.urls import path
from . import views

app_name = 'recommendations'

urlpatterns = [
    path('',           views.home,      name='home'),
    path('recommend/', views.recommend, name='recommend'),
]
