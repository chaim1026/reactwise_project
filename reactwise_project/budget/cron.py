# on the first every month
from .models import Expenses
from crum import get_current_user
from django.utils import timezone
import datetime

# if its the new year fix that 
expenses = Expenses.objects.filter(user=get_current_user(), category='annual', date__month=(datetime.date.today().month - 1), date__year=datetime.date.today().year)
for expense in expenses:
    monthly_annual = Expenses(name=expense.name, amount=expense.amount, category=expense.category, user=expense.user, date=timezone.now(), status='disapprove')
    monthly_annual.save()




# code that asks the user if he moved over the annual and if yes changes the newly added annual expenses from disapproved to approved

