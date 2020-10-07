from django import forms
from .models import Expenses, MoneySpent, Budget, Bot, BotUnexpectedExpense, BotExpenseBalance, BotExpenseInput
from django.contrib.auth.models import User


class ExpensesForm(forms.ModelForm):

    class Meta:      
        model = Expenses
        fields = '__all__'
        exclude = ['user', 'date', 'status']


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


class BotUnexpectedExpenseForm(forms.ModelForm):
    class Meta:
        model = BotUnexpectedExpense
        fields = '__all__'
        exclude = ['user', 'date']


class BotExpenseBalanceForm(forms.ModelForm):
    class Meta:
        model = BotExpenseBalance
        fields = '__all__'
        exclude = ['user', 'date']


class BotExpenseInputForm(forms.ModelForm):
    class Meta:
        model = BotExpenseInput
        fields = '__all__'
        exclude = ['user', 'date']