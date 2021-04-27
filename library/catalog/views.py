from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import RegistrationForm, EditProfileForm, ChangePasswordForm
from .models import Book, Review, User
from mongoengine.queryset.visitor import Q
from werkzeug.security import generate_password_hash

_id = '606ecd74e5fd490b3c6d0657'


def profile_details(request):
    user = User.objects(id=_id).first()
    return render(request, 'profile_details.html', {'user': user})


def profile_edit(request):
    user = User.objects(id=_id).first()
    data = {
        'firstname': user.firstname,
        'lastname': user.lastname,
        'email': user.email,
        'login': user.login,
    }
    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        if form.is_valid():
            firstname = form.cleaned_data.get('firstname')
            lastname = form.cleaned_data.get('lastname')
            email = form.cleaned_data.get('email')
            login = form.cleaned_data.get('login')
            user.update(
                firstname=firstname,
                lastname=lastname,
                email=email,
                login=login
            )
            return redirect(profile_details)
    else:
        form = EditProfileForm(initial=data)
    return render(request, 'profile_edit.html', {'user': user, 'form': form})


def change_password(request):
    user = User.objects(id=_id).first()
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data.get('old_password')
            new_password = form.cleaned_data.get('new_password')
            confirm_password = form.cleaned_data.get('confirm_password')
            return redirect(profile_details)
    else:
        form = ChangePasswordForm()
    return render(request, 'change_password.html', {'user': user, 'form': form})


def book_details(request, book_id):
    # book_id = '60610c2952cd4157727d8ee3'
    book = Book.objects(id=book_id).first()
    reviews = Review.objects(book_id=book_id)
    return render(request, 'book-details.html', {'book': book, 'reviews': reviews})


def home(request):
    top_books = Book.objects.filter(statistic__rating__gte=4.5)[:5]
    new_books = Book.objects.order_by('-id')[:10]
    return render(request, 'home.html', {'top_books': top_books, 'new_books': new_books})


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
