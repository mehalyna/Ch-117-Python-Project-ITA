from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from mongoengine.queryset.visitor import Q

from .forms import RegistrationForm
from .models import Book, Review, MongoUser


def change_password(request):
    return render(request, 'change_password.html')


def book_details(request, book_id):
    # book_id = '60610c2952cd4157727d8ee3'
    book = Book.objects(id=book_id).first()
    reviews = Review.objects(book_id=book_id)
    return render(request, 'book-details.html', {'book': book, 'reviews': reviews})


def home(request):
    top_books = Book.objects.filter(statistic__rating__gte=4.5)[:10]
    new_books = Book.objects.order_by('-id')[:10]
    return render(request, 'home.html', {'top_books': top_books, 'new_books': new_books})


def category_search(request, genre):
    books = Book.objects.filter(genres=genre)
    return render(request, 'books.html', {'books': books})
  

def base(request):
    return render(request, 'base.html')


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = MongoUser(email=form.cleaned_data.get('email'))
            user.first_name = form.cleaned_data.get('firstname')
            user.last_name = form.cleaned_data.get('lastname')
            user.username = form.cleaned_data.get('login')
            user.set_password(form.cleaned_data.get('password'))
            user.save()

            return redirect(home)
    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})


def unique_registration_check(request, field_value):
    user = User.objects(Q(login=field_value) | Q(email=field_value))
    if user:
        return HttpResponse('Already taken', content_type="text/plain")
    return HttpResponse('', content_type="text/plain")


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


@login_required
def profile_details(request):
    return render(request, 'profile_details.html')


@login_required
def profile_edit(request):
    return render(request, 'profile_edit.html')
