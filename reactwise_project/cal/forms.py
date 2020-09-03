from django import forms
from .models import CalSpending
from django.contrib.auth.models import User


class CalSpendingForm(forms.ModelForm):

    class Meta:      
        model = CalSpending
        fields = '__all__'
        exclude = ['user']