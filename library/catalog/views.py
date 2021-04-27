from django.http import HttpResponse
from django.shortcuts import redirect, render
from mongoengine.queryset.visitor import Q
from werkzeug.security import generate_password_hash

from .forms import RegistrationForm
from .models import Book, Review, User


def profile_details(request):
    return render(request, 'profile_details.html')


def profile_edit(request):
    return render(request, 'profile_edit.html')


def change_password(request):
    return render(request, 'change_password.html')


def book_details(request, book_id):
    # book_id = '60610c2952cd4157727d8ee3'
    book = Book.objects(id=book_id).first()
    reviews = Review.objects(book_id=book_id)
    return render(request, 'book-details.html', {'book': book, 'reviews': reviews})


def home(request):
    return render(request, 'home.html')
  

def base(request):
    return render(request, 'base.html')


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User(email=form.cleaned_data.get('email'))
            user.firstname = form.cleaned_data.get('firstname')
            user.lastname = form.cleaned_data.get('lastname')
            user.login = form.cleaned_data.get('login')
            user.password_hash = generate_password_hash(form.cleaned_data.get('password'))
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
