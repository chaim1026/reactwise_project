from django.urls import path
from . import views


urlpatterns = [
    path('submit-spending/', views.spending, name='spending'),
    path('calendar/', views.CalendarView.as_view(), name='calendar'), 
]