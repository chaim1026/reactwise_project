from django.shortcuts import render, redirect
from .models import Daily, Monthly, Annual, MoneySpent
from django.contrib.auth.models import User
from .forms import DailyForm, MonthlyForm, AnnualForm, MoneySpentForm
from django.contrib import messages
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from django.db.models import Avg, Max, Min, Sum
from django.db.models.functions import Coalesce
import datetime

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
            return render(request, 'homepage.html')
        else:
            messages.warning(request, 'Please correct the errors below.')
            return render(request, 'forms.html', context = {'daily_form': DailyForm(), 'monthly_form': MonthlyForm(), 'annual_form': AnnualForm()})



def daily_spending(request):
    daily_info = Daily.objects.get(user_id = request.user)
    weekly = daily_info.weekly/4
    if request.method == "POST":
        spent_form = MoneySpentForm(request.POST)
        if spent_form.is_valid():
            spent = spent_form.save(commit=False) 
            spent.user = request.user
            spent.save()
            return redirect('daily')
    total_sum = MoneySpent.objects.filter(user=request.user, date__month=datetime.date.today().month, date__year=datetime.date.today().year ).aggregate(total_sum=Coalesce(Sum('spent'), 0))['total_sum']
    sundays = get_sundays()
    total_sum_weekly = MoneySpent.objects.filter(user=request.user, date__gte=sundays[0], date__lt=sundays[1]).aggregate(total_sum=Coalesce(Sum('spent'), 0))['total_sum']
    # total_sum = Coalesce(sum(sum_of_spending.values()), 0)
    # try:
    #     total_sum = sum(sum_of_spending.values())
    # except:
    #     total_sum = 0
    labels = ['Available', 'Spent']
    fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
    fig.add_trace(go.Pie(labels=labels, values=[weekly - total_sum_weekly, total_sum_weekly], name="Weekly Chart"), 1, 1)
    fig.add_trace(go.Pie(labels=labels, values=[daily_info.weekly - total_sum, total_sum], name="Monthly Chart"), 1, 2)
    fig.update_traces(hole=.8, hoverinfo="label+percent+name")
    fig.update_layout(annotations=[dict(text=f'spent: {total_sum}', x=0.20, y=0.5, font_size=20, showarrow=False), dict(text=f'spent: {total_sum}', x=0.80, y=0.5, font_size=20, showarrow=False)])
    chart = fig.to_html(full_html=False)
    return render(request, 'daily.html', context = {'daily_info': daily_info, 'weekly': weekly, 'chart': chart, 'spent_form': MoneySpentForm(), 'sum_of_spending': total_sum})



def monthly_spending(request):
    monthly_sum = Monthly.objects.get(user_id = request.user)
    monthly_sum.sum_of_monthly_expenses()
    return render(request, 'monthly.html', context = {'sum': monthly_sum})


def annual_spending(request):
    annual_sum = Annual.objects.get(user_id = request.user)
    annual_sum.sum_of_annual_expenses()
    return render(request, 'annual.html', context = {'sum': annual_sum})


def month_end(request):
    return render(request, 'month_end.html')


def homepage(request):
    return render(request, 'homepage.html')