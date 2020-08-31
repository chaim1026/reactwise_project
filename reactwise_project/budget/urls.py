from django.urls import path
from . import views

urlpatterns = [
    path('forms/', views.forms, name = 'forms'),
    path('additional-expenses-form/', views.additional_expenses_form, name = 'additional_expenses_form'),
    path('homepage/', views.homepage, name = 'homepage'),
    path('Daily-Spending/', views.daily_spending, name = 'daily'),
    path('Monthly-Spending/', views.monthly_spending, name = 'monthly'),
    path('Monthly-Spreadsheet/', views.monthly_spreadsheet, name = 'monthly_spreadsheet'),
    path('Annual-Spending/', views.annual_spending, name = 'annual'),
    path('Annual-Spreadsheet/', views.annual_spreadsheet, name = 'annual_spreadsheet'),
    path('Month-Summary/', views.month_summary, name = 'month_summary'),
    path('Budget/', views.budget, name = 'budget'),
]