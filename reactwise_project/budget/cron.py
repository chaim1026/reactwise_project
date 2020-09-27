# on the first every month
import os
import django
import json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reactwise_project.settings')
django.setup()
from .models import Expenses
from crum import get_current_user
from django.utils import timezone
import datetime


# if its the new year fix that 
def my_cron_job():
    # for user in users
    if statement
    expenses = Expenses.objects.filter(category='annual', date__month=(datetime.date.today().month - 1), date__year=datetime.date.today().year)
    for expense in expenses:
        new_expense = expense
        new_expense.pk = None
        new_expense.status = 'disapproved'
        new_expense.date = timezone.now()
        new_expense.save()








# code that asks the user if he moved over the annual and if yes changes the newly added annual expenses from disapproved to approved

