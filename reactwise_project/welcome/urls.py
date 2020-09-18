from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('success/', views.success, name='success'),
    path('how-it-works/', views.how_it_works, name='how_it_works'),
    path('reactcard/', views.reactcard, name='reactcard'),
]