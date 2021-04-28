import json

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render
from mongoengine.queryset.visitor import Q
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm
from .models import Book, MongoUser, Review





def change_password(request):
    return render(request, 'change_password.html')


def book_details(request, book_id):
    # book_id = '60610c2952cd4157727d8ee3'
    book = Book.objects(id=book_id).first()
    return render(request, 'book-details.html', {'book': book})


def home(request):
    return render(request, 'home.html')
  

def base(request):
    return render(request, 'base.html')


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = MongoUser(email=form.cleaned_data.get('email'))
            user.firstname = form.cleaned_data.get('firstname')
            user.lastname = form.cleaned_data.get('lastname')
            user.login = form.cleaned_data.get('login')
            user.password_hash = generate_password_hash(form.cleaned_data.get('password'))
            user.save()

            return redirect(home)
    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request=request, username=username, password=password)
        if user:
            login(request, user)
        print(user.is_authenticated)
    return redirect(home)


def logout_view(request):
    logout(request)
    return redirect(home)


def func_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')
        user = authenticate(request=request, username=username, password=password)
        print(user.firstname)
        if user:
            login(request, user)
            print(user.is_authenticated)
        return HttpResponse(json.dumps({"message": "Success"}), content_type="application/json")
    return HttpResponse(json.dumps({"message": "Denied"}), content_type="application/json")


@login_required
def profile_details(request):
    return render(request, 'profile_details.html')


@login_required
def profile_edit(request):
    return render(request, 'profile_edit.html')
