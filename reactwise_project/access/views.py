from django.shortcuts import render, HttpResponse, redirect
from .forms import UserSignupForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

def signup(request):
    if request.method == 'GET':    
        signup_form = UserSignupForm()
        return render(request, 'signup.html', {'signup_form': signup_form})

    if request.method == 'POST':
        signup_form = UserSignupForm(request.POST)
        if signup_form.is_valid():
            new_user = signup_form.save()
            login(request, new_user)
            return redirect('forms')
    return render(request, 'signup.html', {'signup_form': signup_form})