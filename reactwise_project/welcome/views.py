from django.shortcuts import render

def welcome(request):
    return render(request, 'welcome.html')


def how_it_works(request):
    return render(request, 'how_it_works.html')


def reactcard(request):
    return render(request, 'reactcard.html')
