from django.shortcuts import render, redirect
from .models import Daily, Monthly, Annual, Additional_expenses, MoneySpent, Budget, Bot
from django.contrib.auth.models import User
from .forms import DailyForm, MonthlyForm, AnnualForm, Additional_expensesForm, MoneySpentForm, BudgetForm, BotForm
from django.contrib import messages
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from django.db.models import Avg, Max, Min, Sum
from django.db.models.functions import Coalesce
import datetime
from chatterbot import ChatBot 
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer


def get_sundays():
    today = datetime.date.today()
    idx = (today.weekday() + 1) % 7
    sun = today - datetime.timedelta(idx)
    next_sun = today + datetime.timedelta(idx)
    if next_sun == sun:
	    next_sun = today + datetime.timedelta(7 + idx)
    return sun, next_sun
    


def forms(request):
    if request.method == "GET":
        return render(request, 'forms.html', context = {'daily_form': DailyForm(), 'monthly_form': MonthlyForm(), 'annual_form': AnnualForm()})

    if request.method == "POST":
        daily_form = DailyForm(request.POST)
        monthly_form = MonthlyForm(request.POST)
        annual_form = AnnualForm(request.POST)
        if daily_form.is_valid() and monthly_form.is_valid() and annual_form.is_valid():
            daily = daily_form.save(commit=False) 
            monthly = monthly_form.save(commit=False) 
            annual = annual_form.save(commit=False)
            daily.user = request.user
            monthly.user = request.user
            annual.user = request.user
            daily.save() 
            monthly.save() 
            annual.save()
            return redirect('additional_expenses_form')
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, 'forms.html', context = {'daily_form': DailyForm(), 'monthly_form': MonthlyForm(), 'annual_form': AnnualForm()})


def additional_expenses_form(request):
    if request.method == 'GET':
        return render(request, 'additional_expenses_form.html', context = {'additional_form': Additional_expensesForm()})

    if request.method == 'POST':
        additional_form = Additional_expensesForm(request.POST)
        if additional_form.is_valid():
            additional = additional_form.save(commit=False)
            additional.user = request.user
            additional.save()
            return redirect('additional_expenses_form')
        else:
            messages.error(request, 'Please correct the errors below.')
            return render(request, 'additional_expenses_form.html', context = {'additional_form': Additional_expensesForm()})
            


def daily_spending(request):
    daily_info = Daily.objects.get(user= request.user, date__month=datetime.date.today().month, date__year=datetime.date.today().year)
    additional_expenses = Additional_expenses.objects.filter(user= request.user, date__month=datetime.date.today().month, date__year=datetime.date.today().year)
    sum_of_additional_expenses = 0
    for expense in additional_expenses:
        if expense.category == 'daily':
            sum_of_additional_expenses += expense.amount
    weekly = daily_info.weekly/4 + sum_of_additional_expenses/4
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
    fig.add_trace(go.Pie(labels=labels, values=[(daily_info.weekly + sum_of_additional_expenses) - total_sum_monthly, total_sum_monthly], name="Monthly Chart"), 1, 2)
    fig.update_traces(hole=.8, hoverinfo="label+percent+name")
    fig.update_layout(annotations=[dict(text=f'spent: {total_sum_weekly}', x=0.20, y=0.5, font_size=20, showarrow=False), dict(text=f'spent: {total_sum_monthly}', x=0.80, y=0.5, font_size=20, showarrow=False)])
    chart = fig.to_html(full_html=False)
    return render(request, 'daily.html', context = {'daily_info': daily_info, 'weekly': weekly, 'chart': chart, 'spent_form': MoneySpentForm(), 'sum_of_spending': total_sum_monthly, 'sum_of_additional_expenses': sum_of_additional_expenses, 'additional_expenses': additional_expenses})



def monthly_spending(request):
    monthly = Monthly.objects.get(user= request.user, date__month=datetime.date.today().month, date__year=datetime.date.today().year)
    additional_monthly = Additional_expenses.objects.filter(user= request.user, date__month=datetime.date.today().month, date__year=datetime.date.today().year)
    sum_of_additional_expenses = 0
    for expense in additional_monthly:
        if expense.category == 'monthly':
            sum_of_additional_expenses += expense.amount
    return render(request, 'monthly.html', context = {'monthly': monthly, 'additional_monthly': additional_monthly, 'sum_of_additional_expenses': sum_of_additional_expenses})


def monthly_spreadsheet(request):
    monthly = Monthly.objects.filter(user=request.user, date__year=datetime.date.today().year)
    additional_monthly = Additional_expenses.objects.filter(user= request.user, date__year=datetime.date.today().year)
    return render(request, 'monthly_spreadsheet.html', context = {'mss': monthly, 'additional_monthly': additional_monthly})


def annual_spending(request):
    annual = Annual.objects.get(user=request.user, date__month=datetime.date.today().month, date__year=datetime.date.today().year)
    additional_annual = Additional_expenses.objects.filter(user=request.user, date__month=datetime.date.today().month, date__year=datetime.date.today().year)
    sum_of_additional_expenses = 0
    for expense in additional_annual:
        if expense.category == 'annual':
            sum_of_additional_expenses += expense.amount
    return render(request, 'annual.html', context = {'annual': annual, 'additional_annual': additional_annual, 'sum_of_additional_expenses': sum_of_additional_expenses})


def annual_spreadsheet(request):
    annual = Annual.objects.filter(user=request.user, date__year=datetime.date.today().year)
    additional_annual = Additional_expenses.objects.filter(user=request.user, date__year=datetime.date.today().year)
    return render(request, 'annual_spreadsheet.html', context = {'ass': annual, 'additional_annual': additional_annual})


def month_summary(request):
    daily = Daily.objects.get(user= request.user, date__month=datetime.date.today().month, date__year=datetime.date.today().year)
    monthly = Monthly.objects.get(user= request.user, date__month=datetime.date.today().month, date__year=datetime.date.today().year)
    annual = Annual.objects.get(user= request.user, date__month=datetime.date.today().month, date__year=datetime.date.today().year)
    additional_expenses = Additional_expenses.objects.filter(user= request.user, date__month=datetime.date.today().month, date__year=datetime.date.today().year)
    user_budget = Budget.objects.filter(user= request.user, date__month=datetime.date.today().month, date__year=datetime.date.today().year)
    budget_sum = 0
    for budget in user_budget:
        budget_sum += budget.amount
    sum_of_additional_daily = 0
    sum_of_additional_monthly = 0
    sum_of_additional_annual = 0
    for expense in additional_expenses:
        if expense.category == 'daily':
            sum_of_additional_daily += expense.amount
        elif expense.category == 'monthly':
            sum_of_additional_monthly += expense.amount
        else:
            sum_of_additional_annual += expense.amount
    total_expenses = sum_of_additional_daily + sum_of_additional_monthly + sum_of_additional_annual + daily.sum_of_daily() + monthly.sum_of_monthly_expenses() + annual.sum_of_annual_expenses()
    outcome = budget_sum - total_expenses
    return render(request, 'month_summary.html', context = {'daily': daily, 'monthly': monthly, 'annual': annual, 'sum_of_additional_daily': sum_of_additional_daily, 'sum_of_additional_monthly': sum_of_additional_monthly, 'sum_of_additional_annual': sum_of_additional_annual, 'budget_sum': budget_sum, 'total_expenses': total_expenses, 'outcome': outcome})


def homepage(request):
    date = datetime.datetime.today().day   
    messages.info(request, 'Please fill out your new forms')
    
    # my_bot = ChatBot(name='PyBot', read_only=True, logic_adapters=['chatterbot.logic.MathematicalEvaluation', 'chatterbot.logic.BestMatch'])

    # small_talk = ['hi there',
    #     'how do you do?',
    #     'how are you?',
    #     'i\'m cool.',
    #     'fine, you?',
    #     'always cool',
    #     'i\'m ok',
    #     'glad to hear that',
    #     'i feel awesome',
    #     'excellent, glad to hear that',
    #     'not so good',
    #     'sorry to hear that.',
    #     'what\'s your name?',
    #     'i\'m pybot. ask me a math question, please.']

    # math_talk_1 = ['pythagorean theorem', 'a squared plus b squared equals c squared.']

    # math_talk_2 = ['law of cosines', 'c**2 = a**2 + b**2 - 2 * a * b * cos(gamma)']

    # list_trainer = ListTrainer(my_bot)

    # corpus_trainer = ChatterBotCorpusTrainer(my_bot)
    # corpus_trainer.train('chatterbot.corpus.english')

    # for item in (small_talk, math_talk_1, math_talk_2):
    #     list_trainer.train(item)

    # if request.method == "GET":
    #     return render(request, 'homepage.html', context={'date': date, 'bot': my_bot, 'bot_form': BotForm(), 'showdiv': False})

    # if request.method == "POST":
    #     robot_form = BotForm(request.POST)
    #     if robot_form.is_valid():
    #         r_form = robot_form.save(commit=False)
    #         text = r_form.text
    #         text = my_bot.get_response(text)
    #         # r_form.save()
    #         # return redirect('robot')
    #         return render(request, 'robot.html', context={'bot': my_bot, 'bot_form': BotForm(), 'text': text, 'showdiv': True })

    return render(request, 'homepage.html', context = {'date': date, 'bot_form': BotForm()})


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
