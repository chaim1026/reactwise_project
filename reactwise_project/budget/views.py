from django.shortcuts import render, redirect
from .models import Expenses, MoneySpent, Budget, Bot
from django.contrib.auth.models import User
from .forms import ExpensesForm, MoneySpentForm, BudgetForm, BotForm
from django.contrib import messages
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from django.db.models import Avg, Max, Min, Sum
from django.db.models.functions import Coalesce
import datetime
from chatterbot import ChatBot 
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
from django.contrib.auth.decorators import login_required



def get_sundays():
    today = datetime.date.today()
    idx = (today.weekday() + 1) % 7
    sun = today - datetime.timedelta(idx)
    next_sun = today + datetime.timedelta(idx)
    if next_sun == sun:
	    next_sun = today + datetime.timedelta(7 + idx)
    return sun, next_sun
    

@login_required
def expenses_forms(request):
    expenses = Expenses.objects.filter(user= request.user, date__month=datetime.date.today().month, date__year=datetime.date.today().year)

    if request.method == 'GET':
        return render(request, 'expenses_form.html', context={'expenses': expenses, 'expenses_form': ExpensesForm()})
    
    if request.method == 'POST':
        expenses_form = ExpensesForm(request.POST)
        if expenses_form.is_valid():
            expenses = expenses_form.save(commit=False)
            expenses.user = request.user
            expenses.save()
            return redirect('expenses_form')
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, 'expenses_form.html', context={'expenses': expenses, 'expenses_form': ExpensesForm()})


@login_required
def daily_spending(request):
    daily_info = Expenses.objects.filter(user= request.user, category='daily', date__month=datetime.date.today().month, date__year=datetime.date.today().year)
    sum_daily = 0
    weekly = 0
    for expense in daily_info:
        sum_daily += expense.amount
        if expense.name == 'weekly':
            weekly += expense.amount
    full_weekly = weekly
    weekly = weekly/4
    if request.method == "POST":
        spent_form = MoneySpentForm(request.POST)
        if spent_form.is_valid():
            spent = spent_form.save(commit=False) 
            spent.user = request.user
            sundays = get_sundays()
            total_sum_weekly = MoneySpent.objects.filter(user=request.user, date__gte=sundays[0], date__lt=sundays[1]).aggregate(total_sum_monthly=Coalesce(Sum('spent'), 0))['total_sum_monthly'] + spent.spent
            if total_sum_weekly > weekly:
                messages.warning(request, 'With that charge you are exceeding your weekly budget!!!')
                return redirect('daily')
            else:
                spent.save()
                return redirect('daily')
    total_sum_monthly = MoneySpent.objects.filter(user=request.user, date__month=datetime.date.today().month, date__year=datetime.date.today().year ).aggregate(total_sum_monthly=Coalesce(Sum('spent'), 0))['total_sum_monthly']
    sundays = get_sundays()
    total_sum_weekly = MoneySpent.objects.filter(user=request.user, date__gte=sundays[0], date__lt=sundays[1]).aggregate(total_sum_monthly=Coalesce(Sum('spent'), 0))['total_sum_monthly']
    labels = ['Available', 'Spent']
    fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
    fig.add_trace(go.Pie(labels=labels, values=[weekly - total_sum_weekly, total_sum_weekly], name="Weekly Chart"), 1, 1)
    fig.add_trace(go.Pie(labels=labels, values=[full_weekly - total_sum_monthly, total_sum_monthly], name="Monthly Chart"), 1, 2)
    fig.update_traces(hole=.8, hoverinfo="label+percent+name")
    fig.update_layout(annotations=[dict(text=f'spent: {total_sum_weekly}', x=0.20, y=0.5, font_size=20, showarrow=False), dict(text=f'spent: {total_sum_monthly}', x=0.80, y=0.5, font_size=20, showarrow=False)])
    chart = fig.to_html(full_html=False)
    return render(request, 'daily.html', context = {'daily_info': daily_info, 'weekly': weekly, 'full_weekly':full_weekly, 'chart': chart, 'spent_form': MoneySpentForm(), 'sum_of_spending': total_sum_monthly, 'sum_daily': sum_daily})


@login_required
def monthly_spending(request):
    monthly = Expenses.objects.filter(user= request.user, category='monthly', date__month=datetime.date.today().month, date__year=datetime.date.today().year)
    sum_monthly = 0
    for expense in monthly:
        sum_monthly += expense.amount
    return render(request, 'monthly.html', context = {'monthly': monthly, 'sum_monthly': sum_monthly})

@login_required
def monthly_spreadsheet(request):
    monthly = Expenses.objects.filter(user=request.user, category='monthly', date__year=datetime.date.today().year)
    month_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    let_month_list = ['January', 'Febuary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    return render(request, 'monthly_spreadsheet.html', context = {'mss': monthly, 'month_list': month_list, 'let_month_list': let_month_list, 'zip': zip(range(1,13),let_month_list)})

@login_required
def annual_spending(request):
    annual = Expenses.objects.filter(user=request.user, category='annual', date__month=datetime.date.today().month, date__year=datetime.date.today().year)
    sum_annual = 0
    for expense in annual:
        sum_annual += expense.amount
    return render(request, 'annual.html', context = {'annual': annual, 'sum_annual': sum_annual})

@login_required
def annual_spreadsheet(request):
    annual = Expenses.objects.filter(user=request.user, category='annual', date__year=datetime.date.today().year)
    month_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    let_month_list = ['January', 'Febuary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    return render(request, 'annual_spreadsheet.html', context = {'ass': annual, 'month_list': month_list, 'let_month_list': let_month_list, 'range': range(1,13), 'zip': zip(range(1,13),let_month_list)})


@login_required
def month_summary(request):
    expenses = Expenses.objects.filter(user= request.user, date__month=datetime.date.today().month, date__year=datetime.date.today().year)
    user_budget = Budget.objects.filter(user= request.user, date__month=datetime.date.today().month, date__year=datetime.date.today().year)
    budget_sum = 0
    for budget in user_budget:
        budget_sum += budget.amount
    sum_daily = 0
    sum_monthly = 0
    sum_annual = 0
    for expense in expenses:
        if expense.category == 'daily':
            sum_daily += expense.amount
        elif expense.category == 'monthly':
            sum_monthly += expense.amount
        else:
            sum_annual += expense.amount
    total_expenses = sum_daily + sum_monthly + sum_annual
    outcome = budget_sum - total_expenses
    return render(request, 'month_summary.html', context = {'sum_daily': sum_daily, 'sum_monthly': sum_monthly, 'sum_annual': sum_annual, 'budget_sum': budget_sum, 'total_expenses': total_expenses, 'outcome': outcome})

@login_required
def homepage(request):
    date = datetime.datetime.today().day   
    messages.info(request, 'Please fill out your new forms')
    annual = Expenses.objects.filter(user=request.user, category='annual', date__month=datetime.date.today().month, date__year=datetime.date.today().year)
    name_list = []
    num_list = []
    final_list = []
    for expense in annual:
        name_list.append(expense.name)
    for expense in annual:
        num_list.append(expense.amount)
    for i, y in zip(name_list,num_list):
        final_list.append(i+':  '+str(y))

    if request.method == "GET":
        return render(request, 'homepage.html', context={'n': name_list, 'date': date, 'bot_form': BotForm(), 'showdiv': False})
     

    if request.method == "POST":
        robot_form = BotForm(request.POST)
        if robot_form.is_valid():
            r_form = robot_form.save(commit=False)
            r_form.user = request.user
            text = r_form.text
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
                reply = '\n'.join(map(str, final_list)) +'\n'+'\n'+ 'Where would you like to deduct your expense' 
                reply = reply.upper()
            r_form.save()
            return render(request, 'homepage.html', context={'n': name_list, 'annual': annual, 'bot_form': BotForm(), 'text': text, 'reply': reply, 'showdiv': True})

    return render(request, 'homepage.html', context = {'n': name_list, 'date': date, 'bot_form': BotForm(), 'd': deduct_from})

@login_required
def budget(request):
    user_budget = Budget.objects.filter(user= request.user, date__month=datetime.date.today().month, date__year=datetime.date.today().year)
    budget_sum = 0
    for budget in user_budget:
        budget_sum += budget.amount

    if request.method == 'GET':
        return render(request, 'budget.html', context = {'budget_form': BudgetForm(), 'user_budget': user_budget, 'budget_sum': budget_sum})

    if request.method == 'POST':
        budget_form = BudgetForm(request.POST)
        if budget_form.is_valid():
            the_budget = budget_form.save(commit=False)
            the_budget.user = request.user
            the_budget.save()
            return redirect('budget')
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, 'budget.html', context = {'budget_form': BudgetForm(), 'user_budget': user_budget, 'budget_sum': budget_sum})
