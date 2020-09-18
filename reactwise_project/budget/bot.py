from .models import Expenses
from crum import get_current_user
from django.utils import timezone
import datetime
from django.db.models import Sum



annual = Expenses.objects.filter(user=request.user, category='annual', date__month=datetime.date.today().month, date__year=datetime.date.today().year)
name_list = []

for expense in annual:
    name_list.append(expense.name)

# 3 things will go here 

# 1 get the total of a certan expense in annual
# 2 make a deduction when getting a unexpected expense from daily or from annual 
# 3 input an expense that was from annual

# after Annual Expense Balance is pressed get the balance of a specific annual expense
# ask user which expense balance he wants to check
reply = ('\n' + 'Which expense balance would you like to see?' +'\n'+'\n'+'\n'.join(map(str, name_list))).upper()
while text.lower() != 'done':
    if text in name_list:
        annual_expenses = Expenses.objects.filter(user=get_current_user(), name=text, category='annual', status='approved').aggregate(Sum('amount'))
        reply = annual_expenses
    else:
        reply = 'Expense does not exist'



# after annual expense spent is pressed
reply = 'What is the name of your expense spent?'
while text != 'done'


# after Unexpected Expense is pressed 
reply = 'HOW MUCH IS THE EXPENSE?'
while text.lower() != 'done':




name_list = []
    num_list = []
    final_list = []
    for expense in annual:
        name_list.append(expense.name)
    for expense in annual:
        num_list.append(expense.amount)
    for i, y in zip(name_list,num_list):
        final_list.append(i+':  '+str(y))

if text == 'yes':
                reply = 'HOW MUCH IS THE EXPENSE?'
            elif text in name_list:
                for expense in annual:
                    if expense.name == text:
                        amount_update = expense.amount
                bot_txt = Bot.objects.filter(user=request.user, date__month=datetime.date.today().month, date__year=datetime.date.today().year)
                for txt in bot_txt:
                    num_deduct = txt.text
                name_update = text
                update = amount_update - int(num_deduct)
                Expenses.objects.filter(user=request.user, category='annual', name=name_update, date__month=datetime.date.today().month, date__year=datetime.date.today().year).update(amount=update)
                reply = 'ok just updated your expense do u have any other expenses?'.upper()           
            else:
                reply = ('\n'.join(map(str, final_list)) +'\n'+'\n'+ 'Where would you like to deduct your expense').upper()
            