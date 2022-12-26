from django.contrib import auth
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


# Create your views here.

def index(request):
    return render(request, 'index.html')


def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    print(username, password)

    user = authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return render(request, 'index.html')
    else:
        return render(request, 'index.html', {'error': 'Nombre de usuario o contraseña incorrectos'})


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
