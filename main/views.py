from django.contrib import auth, messages
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


# Create your views here.

def index(request):
    return render(request, 'index.html')


def register(request):
    username = request.POST['username']
    password = request.POST['password']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']

    errors = []
    if username == " " or password == " " or first_name == " " or last_name == " " or email == " ":  # Check if any field is empty
        empty = "Todos los campos del formulario deben estar rellenos"
        errors.append(empty)
    if first_name[0].islower():
        first_letter_name = "La primera letra del nombre debe ser mayúscula"
        errors.append(first_letter_name)
    if last_name[0].islower():
        first_letter_surname = "La primera letra del apellido debe ser mayúscula"
        errors.append(first_letter_surname)
    if len(password) < 8:
        password_length = "La contraseña debe tener al menos 8 caracteres"
        errors.append(password_length)
    if len(username) < 4:
        username_length = "El nombre de usuario debe tener al menos 4 caracteres"
        errors.append(username_length)

    user_username = User.objects.filter(username=username)
    user_email = User.objects.filter(email=email)

    if user_username:
        username_exists = "El nombre de usuario ya existe"
        errors.append(username_exists)
    if user_email:
        email_exists = "El email ya existe"
        errors.append(email_exists)

    if len(errors) > 0:
        are_errors = True
        return render(request, 'index.html', {
            "errors": errors,
            "username": username,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "are_errors": are_errors
        })
    else:
        user = User.objects.create_user(username=username,
                                        password=password,
                                        first_name=first_name,
                                        last_name=last_name, email=email)
        user.save()
        auth.login(request, user)
        return HttpResponseRedirect(reverse("index"))


def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect(reverse('index'))
    else:
        messages.error(request, 'Credenciales incorrectas')
        return HttpResponseRedirect(reverse('index'))


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
