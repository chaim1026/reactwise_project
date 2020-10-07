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
from django.contrib.auth.models import User
from .models import Expenses



def my_cron_job():
    users = User.objects.all()
    for user in users:
        if datetime.date.today().month == 1:
            year = (datetime.date.today().year - 1)
            month = 12
        else:
            year = datetime.date.today().year
            month = (datetime.date.today().month - 1)
        expenses = Expenses.objects.filter(user=user.id, category='annual', date__month=month, date__year=year)
        for expense in expenses:
            if expense.amount > 0:
                new_expense = expense
                new_expense.pk = None
                new_expense.status = 'disapproved'
                new_expense.date = timezone.now()
                new_expense.save()
