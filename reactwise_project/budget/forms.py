from django import forms
from .models import Expenses, MoneySpent, Budget, Bot
from django.contrib.auth.models import User


class ExpensesForm(forms.ModelForm):

    class Meta:      
        model = Expenses
        fields = '__all__'
        exclude = ['user', 'date']


class MoneySpentForm(forms.ModelForm):

    class Meta:      
        model = MoneySpent
        fields = '__all__'
        exclude = ['user', 'date']


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = '__all__'
        exclude = ['user', 'date']


class BotForm(forms.ModelForm):
    class Meta:
        model = Bot
        fields = '__all__'
        exclude = ['user', 'date']