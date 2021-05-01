from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from mongoengine.queryset.visitor import Q
from werkzeug.security import generate_password_hash

from .forms import ChangePasswordForm, EditProfileForm, RegistrationForm
from .models import Book, Review, User, Author

_id = '606ecd74e5fd490b3c6d0657'


def profile_details(request):
    user = User.objects(id=_id).first()
    return render(request, 'profile_details.html', {'user': user})


def profile_bookshelf(request):
    rec_books = Book.objects.filter(statistic__rating__gte=4.5)[:10]
    return render(request, 'profile_bookshelf.html', {'rec_books': rec_books})


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
            if user and user.check_password(old_password):
                new_password = generate_password_hash(form.cleaned_data.get('new_password'))
                user.update(password_hash=new_password)
                messages.success(request, 'Password successfully updated.')
                return redirect(profile_details)
            else:
                messages.success(request, 'Wrong old password.')
    else:
        form = ChangePasswordForm()
    return render(request, 'change_password.html', {'user': user, 'form': form})


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
    return render(request, 'genre-search.html', {'books': books, 'genre': genre})

def form_search(request):
    q = request.GET.get('searchbar', '')
    if q:
        authors = Author.objects(name__icontains=q)
        books_id = []
        for author in authors:
            for book_id in author.books:
                books_id.append(book_id)
        books = Book.objects.filter(Q(title__icontains=q) | Q(year__icontains=q) | Q(id__in=books_id))
    else:
        return render(request, 'books.html')
    return render(request, 'books.html', {'books': books, 'q': q})


def base(request):
    return render(request, 'base.html')


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User(email=form.cleaned_data.get('email').strip())
            user.firstname = form.cleaned_data.get('firstname'.strip())
            user.lastname = form.cleaned_data.get('lastname'.strip())
            user.login = form.cleaned_data.get('login'.strip())
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
