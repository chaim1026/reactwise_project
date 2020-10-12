from django.shortcuts import render, redirect
from .models import Expenses, MoneySpent, Budget, Bot, BotUnexpectedExpense, BotExpenseBalance, BotExpenseInput
from django.contrib.auth.models import User
from .forms import ExpensesForm, MoneySpentForm, BudgetForm, BotForm, BotUnexpectedExpenseForm, BotExpenseBalanceForm, BotExpenseInputForm
from django.contrib import messages
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from django.db.models import Avg, Max, Min, Sum
from django.db.models.functions import Coalesce
import datetime
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from crum import get_current_user
import pyzt


def form_update():
    disapproved = Expenses.objects.filter(user=get_current_user(), date__month=datetime.date.today().month, date__year=datetime.date.today().year, status='disapproved')
    return disapproved

def to_approved():
    annual_expenses = Expenses.objects.filter(user=get_current_user(), date__month=datetime.date.today().month, date__year=datetime.date.today().year, status='disapproved')
    for expense in annual_expenses:
        expense.status = 'approved'
        expense.save()


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
    disapproved = form_update()
    messages.info(request, 'Have you made your monthly transfer to category 3?')
    expenses = Expenses.objects.filter(user=request.user, date__month=datetime.date.today().month, date__year=datetime.date.today().year, status='approved')

    if request.GET.get('cat_3_moved') == 'cat_3_moved':
        to_approved()

    if request.method == 'GET':
        return render(request, 'expenses_form.html', context={'disapproved': disapproved, 'expenses': expenses, 'expenses_form': ExpensesForm()})
    
    if request.method == 'POST':
        expenses_form = ExpensesForm(request.POST)
        if expenses_form.is_valid():
            expenses = expenses_form.save(commit=False)
            expenses.user = request.user
            expenses.save()
            return redirect('expenses_form')
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, 'expenses_form.html', context={'disapproved': disapproved, 'expenses': expenses, 'expenses_form': ExpensesForm()})


@login_required
def daily_spending(request):
    disapproved = form_update()
    messages.info(request, 'Have you made your monthly transfer to category 3?')

    daily_info = Expenses.objects.filter(user= request.user, category='daily', date__month=datetime.date.today().month, date__year=datetime.date.today().year, status='approved')
    sum_daily = 0
    weekly = 0
    for expense in daily_info:
        sum_daily += expense.amount
        if expense.name == 'weekly':
            weekly += expense.amount
    full_weekly = weekly
    weekly = weekly/4

    if request.GET.get('cat_3_moved') == 'cat_3_moved':
        to_approved()

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
    return render(request, 'daily.html', context = {'disapproved': disapproved, 'daily_info': daily_info, 'weekly': weekly, 'full_weekly':full_weekly, 'chart': chart, 'spent_form': MoneySpentForm(), 'sum_of_spending': total_sum_monthly, 'sum_daily': sum_daily})


@login_required
def monthly_spending(request):
    disapproved = form_update()
    messages.info(request, 'Have you made your monthly transfer to category 3?')

    if request.GET.get('cat_3_moved') == 'cat_3_moved':
        to_approved()

    monthly = Expenses.objects.filter(user= request.user, category='monthly', date__month=datetime.date.today().month, date__year=datetime.date.today().year, status='approved')
    sum_monthly = 0
    for expense in monthly:
        sum_monthly += expense.amount
    return render(request, 'monthly.html', context = {'disapproved': disapproved, 'monthly': monthly, 'sum_monthly': sum_monthly})

@login_required
def monthly_spreadsheet(request):
    disapproved = form_update()
    messages.info(request, 'Have you made your monthly transfer to category 3?')
    if request.GET.get('cat_3_moved') == 'cat_3_moved':
        to_approved()

    monthly = Expenses.objects.filter(user=request.user, category='monthly', date__year=datetime.date.today().year, status='approved')
    month_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    let_month_list = ['January', 'Febuary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    return render(request, 'monthly_spreadsheet.html', context = {'disapproved': disapproved, 'mss': monthly, 'month_list': month_list, 'let_month_list': let_month_list, 'zip': zip(range(1,13),let_month_list)})

@login_required
def annual_spending(request):
    disapproved = form_update() 
    messages.info(request, 'Have you made your monthly transfer to category 3?')
    if request.GET.get('cat_3_moved') == 'cat_3_moved':
        to_approved()

    annual = Expenses.objects.filter(user=request.user, category='annual', date__month=datetime.date.today().month, date__year=datetime.date.today().year, status='approved')
    sum_annual = 0
    for expense in annual:
        sum_annual += expense.amount
    return render(request, 'annual.html', context = {'disapproved': disapproved, 'annual': annual, 'sum_annual': sum_annual})

@login_required
def annual_spreadsheet(request):
    disapproved = form_update()
    messages.info(request, 'Have you made your monthly transfer to category 3?')
    if request.GET.get('cat_3_moved') == 'cat_3_moved':
        to_approved()

    annual = Expenses.objects.filter(user=request.user, category='annual', date__year=datetime.date.today().year, status='approved')
    month_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    let_month_list = ['January', 'Febuary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    return render(request, 'annual_spreadsheet.html', context = {'disapproved': disapproved, 'ass': annual, 'month_list': month_list, 'let_month_list': let_month_list, 'range': range(1,13), 'zip': zip(range(1,13),let_month_list)})


@login_required
def month_summary(request):
    disapproved = form_update()
    messages.info(request, 'Have you made your monthly transfer to category 3?')
    if request.GET.get('cat_3_moved') == 'cat_3_moved':
        to_approved()

    expenses = Expenses.objects.filter(user= request.user, date__month=datetime.date.today().month, date__year=datetime.date.today().year, status='approved')
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
    return render(request, 'month_summary.html', context = {'disapproved': disapproved, 'sum_daily': sum_daily, 'sum_monthly': sum_monthly, 'sum_annual': sum_annual, 'budget_sum': budget_sum, 'total_expenses': total_expenses, 'outcome': outcome})

ei_name = ''
ue_name = ''
ue_category = ''
ue_total = 0 
ue_deducted = 0
@login_required
def homepage(request):
    global ei_name
    global ue_name
    global ue_total
    global ue_deducted
    global ue_category
    disapproved = form_update()
    messages.info(request, 'Have you made your monthly transfer to category 3?')
    cat_3 = Expenses.objects.filter(user=request.user, date__month=datetime.date.today().month, date__year=datetime.date.today().year)
    daily = Expenses.objects.filter(user=request.user, category='daily', date__month=datetime.date.today().month, date__year=datetime.date.today().year)
    annual = Expenses.objects.filter(user=request.user, category='annual', date__month=datetime.date.today().month, date__year=datetime.date.today().year)
    name_list = []
    num_list = []
    final_list = []
    for expense in cat_3:
        name_list.append(expense.name)

    if request.GET.get('cat_3_moved') == 'cat_3_moved':
        to_approved()

    if request.method == "GET":
        return render(request, 'homepage.html', context={'disapproved': disapproved, 'hour': timezone.localtime(timezone.now()).hour, 'date''ue_form': BotUnexpectedExpenseForm(), 'eb_form': BotExpenseBalanceForm(), 'ei_form': BotExpenseInputForm(), 'cat_3': cat_3})
     
    if request.method == "POST":
        ue = BotUnexpectedExpenseForm(request.POST)
        if ue.is_valid():
            bue = ue.save(commit=False)
            bue.user = request.user
            unexpected = bue.ue_text
            if unexpected not in name_list and type(int(unexpected)) is int and ue_total == 0:
                ue_total = int(unexpected)
                ue_reply = 'Where would you like to deduct your unexpected expense?'
            elif unexpected in name_list:
                ue_name = unexpected
                if ue_name in daily:
                    ue_category = 'daily'
                else:
                    ue_category = 'annual'
                ue_reply = f'how much of the unexpected expense would you like to deduct from {ue_name.upper()}?'
            elif unexpected not in name_list and type(int(unexpected)) is int and ue_total > 0:
                ue_deducted = int(unexpected)
                if ue_total - ue_deducted > 0:
                    deducted = Expenses(name=ue_name, amount=-(ue_deducted), category=ue_category, date=timezone.now(), user=request.user, status='approved') 
                    deducted.save()
                    ue_reply = f'Deducted {ue_deducted} now {ue_total - ue_deducted} remains from your unexpected expense where would you like to deduct from?'
                    ue_total = ue_total - ue_deducted
                elif ue_total - ue_deducted == 0:
                    deducted = Expenses(name=ue_name, amount=-(ue_deducted), category=ue_category, date=timezone.now(), user=request.user, status='approved') 
                    deducted.save()
                    ue_reply = 'All updated!'
                    ue_total = 0
                elif ue_total - ue_deducted < 0:
                    ue_reply = f'Your deducting more then your standing unexpected expense your expense is {ue_total} dont deduct more!'     
                elif unexpected not in name_list and type(int(unexpected)) is not int:
                    ue_reply = 'Expense does not exist'              
            return render(request, 'homepage.html', context={'hour': timezone.localtime(timezone.now()).hour, 'ue_form': BotUnexpectedExpenseForm(), 'eb_form': BotExpenseBalanceForm(), 'ei_form': BotExpenseInputForm(), 'cat_3': cat_3, 'ue_text': unexpected, 'ue_reply': ue_reply})
    if request.method == "POST":
        eb = BotExpenseBalanceForm(request.POST)
        if eb.is_valid():
            beb = eb.save(commit=False)
            beb.user = request.user
            balance = beb.eb_text
            if balance in name_list:
                annual_expenses = Expenses.objects.filter(user=request.user, name=balance, category='annual', status='approved').aggregate(Sum('amount'))
                eb_reply = annual_expenses['amount__sum']
            elif balance not in name_list:
                eb_reply = 'Expense does not exist'
            return render(request, 'homepage.html', context={'hour': timezone.localtime(timezone.now()).hour, 'ue_form': BotUnexpectedExpenseForm(), 'eb_form': BotExpenseBalanceForm(), 'ei_form': BotExpenseInputForm(), 'cat_3': cat_3, 'eb_reply': eb_reply, 'eb_text': balance})
    if request.method == "POST":
        ei = BotExpenseInputForm(request.POST)
        if ei.is_valid():
            bei = ei.save(commit=False)
            bei.user = request.user
            spent_input = bei.ei_text
            if spent_input in name_list:
                ei_name = spent_input
                ei_reply = 'How much was spent?'
            elif spent_input not in name_list and type(int(spent_input)) is not int:
                ei_reply = 'Expense does not exist'
            elif spent_input not in name_list and type(int(spent_input)) is int:
                input_spent = Expenses(name=ei_name, amount=-(int(spent_input)), category='annual', date=timezone.now(), user=request.user, status='approved') 
                input_spent.save()
                ei_reply = 'All up to date!'           
            return render(request, 'homepage.html', context={'hour': timezone.localtime(timezone.now()).hour, 'ue_form': BotUnexpectedExpenseForm(), 'eb_form': BotExpenseBalanceForm(), 'ei_form': BotExpenseInputForm(), 'cat_3': cat_3, 'ei_reply': ei_reply, 'ei_text': spent_input})

    return render(request, 'homepage.html', context={'disapproved': disapproved, 'hour': timezone.localtime(timezone.now()).hour})


@login_required
def budget(request):
    user_budget = Budget.objects.filter(user= request.user, date__month=datetime.date.today().month, date__year=datetime.date.today().year)
    budget_sum = 0
    disapproved = form_update()
    messages.info(request, 'Have you made your monthly transfer to category 3?')
    if request.GET.get('cat_3_moved') == 'cat_3_moved':
        to_approved()

    for budget in user_budget:
        budget_sum += budget.amount

    if request.method == 'GET':
        return render(request, 'budget.html', context = {'disapproved': disapproved, 'budget_form': BudgetForm(), 'user_budget': user_budget, 'budget_sum': budget_sum})

    if request.method == 'POST':
        budget_form = BudgetForm(request.POST)
        if budget_form.is_valid():
            the_budget = budget_form.save(commit=False)
            the_budget.user = request.user
            the_budget.save()
            return redirect('budget')
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, 'budget.html', context = {'disapproved': disapproved, 'budget_form': BudgetForm(), 'user_budget': user_budget, 'budget_sum': budget_sum})


