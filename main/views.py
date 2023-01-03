from django.contrib import auth, messages
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from main import models
from utils import load_db, whoosh

NUM_ANIMES_PER_PAGE = 36


def index(request):
    if 'search' in request.GET:
        query = request.GET['search']
        if query == "":
            return HttpResponseRedirect(reverse('index'))
        else:
            animes = whoosh.general_search(query)

    else:
        if 'order' in request.GET:
            animes = models.Anime.objects.order_by(request.GET.get('order'))
        else:
            animes = models.Anime.objects.all().order_by('rank')

        if 'genre' in request.GET:
            animes = animes.filter(genres__name=request.GET.get('genre'))

        if 'studio' in request.GET:
            animes = animes.filter(studios__name=request.GET.get('studio'))

        if 'status' in request.GET:
            animes = animes.filter(status__name=request.GET.get('status'))

        if 'type' in request.GET:
            animes = animes.filter(type__name=request.GET.get('type'))

    paginator = Paginator(animes, NUM_ANIMES_PER_PAGE)

    if 'page' in request.GET:
        page_number = request.GET.get('page')
    else:
        page_number = 1

    page_obj = paginator.get_page(page_number)

    genres = models.Genre.objects.all().order_by('name')
    studios = models.Studio.objects.all().order_by('name')
    status = models.Status.objects.all().order_by('name')
    types = models.Type.objects.all().order_by('name')

    return render(request, 'index.html', {'animes': page_obj,
                                          'max_pages': [i for i in range(1, page_obj.paginator.num_pages + 1)],
                                          'genres': genres,
                                          'studios': studios,
                                          'status': status,
                                          'types': types,
                                          'filtros': True})


def custom_search_view(request):
    if request.GET:
        return render(request, 'search.html')
    else:
        animes = []
        if 'phrase' in request.POST:
            phrase = request.POST.get('phrase')
            animes = whoosh.phrase_search(phrase)

        return render(request, 'search.html', {'animes': animes})


def details(request, anime_id):
    anime = models.Anime.objects.get(id=anime_id)
    return render(request, 'details.html', {'anime': anime})


def register(request):
    username = request.POST['username']
    password = request.POST['password']
    first_name = request.POST['first_name']
    last_name = request.POST['last_name']
    email = request.POST['email']

    errors = []
    if username == " " or password == " " or first_name == " " or last_name == " " or email == " ":
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


@login_required
@transaction.atomic
def load_db_whoosh(request):
    try:
        load_db.load()
        return HttpResponse(status=200)
    except:
        return HttpResponse(status=500)
