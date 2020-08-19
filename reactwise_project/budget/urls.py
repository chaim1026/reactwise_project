from django.urls import path
from . import views

urlpatterns = [
    path('forms/', views.forms, name = 'forms'),
    path('homepage/', views.homepage, name = 'homepage'),
    path('Daily-Spending/', views.daily_spending, name = 'daily'),
    path('Monthly-Spending/', views.monthly_spending, name = 'monthly'),
    path('Annual-Spending/', views.annual_spending, name = 'annual'),
    path('Month-End/', views.month_end, name = 'month_end'),
]