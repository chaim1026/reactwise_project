from django.shortcuts import render, redirect
from .models import Contact
from .forms import ContactForm
from django.contrib import messages
from django.core.mail import send_mail, BadHeaderError


def welcome(request):
    if request.method == 'GET':
        return render(request, 'welcome.html', context={'contact_form': ContactForm()})

    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            # c_form = contact_form.save(commit=False)
            subject = contact_form.cleaned_data['name']
            from_email = contact_form.cleaned_data['email']
            message = contact_form.cleaned_data['text']
            try:
                send_mail(subject, message, from_email, ['reactwise@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            contact_form.save()
            return render(request, 'success.html')
        else:
            # messages.error(request, 'Please correct the errors below.')
            print(contact_form.errors)
            return render(request, 'welcome.html', context={'contact_form': ContactForm()})


def success(request):
    return render(request, 'success.html')


def how_it_works(request):
    return render(request, 'how_it_works.html')


def reactcard(request):
    return render(request, 'reactcard.html')
