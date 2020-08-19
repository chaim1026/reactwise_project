from django import forms
from .models import Daily, Monthly, Annual, MoneySpent
from django.contrib.auth.models import User


class DailyForm(forms.ModelForm):

    class Meta:      
        model = Daily
        fields = '__all__'
        exclude = ['user']

class MonthlyForm(forms.ModelForm):

    class Meta:      
        model = Monthly
        fields = '__all__'
        exclude = ['user']



class AnnualForm(forms.ModelForm):

    class Meta:      
        model = Annual
        fields = '__all__'
        exclude = ['user']


class MoneySpentForm(forms.ModelForm):

    class Meta:      
        model = MoneySpent
        fields = '__all__'
        exclude = ['user', 'date']