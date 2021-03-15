from django.shortcuts import render,redirect
from django.http import HttpResponse


#create your views here


def homePage(request):
    if request.user.is_authenticated:
        return redirect('manager:index')

    return render(request, 'index.html')


def aboutPage(request):
    if request.user.is_authenticated:
        return redirect('manager:index')

    return render(request, 'about.html')

def servicesPage(request):
    if request.user.is_authenticated:
        return redirect('manager:index')

    return render(request, 'services.html')

def contactPage(request):
    if request.user.is_authenticated:
        return redirect('manager:index')

    return render(request, 'contact.html')
