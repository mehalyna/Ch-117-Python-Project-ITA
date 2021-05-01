import json

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from mongoengine.queryset.visitor import Q
from werkzeug.security import generate_password_hash

from .forms import ChangePasswordForm, EditProfileForm, RegistrationForm
from .models import Author, Book, Review, MongoUser

_id = '606ecd74e5fd490b3c6d0657'


def profile_details(request):
    user = MongoUser.objects(id=_id).first()
    return render(request, 'profile_details.html', {'user': user})


def profile_bookshelf(request):
    rec_books = Book.objects.filter(statistic__rating__gte=4.5)[:10]
    return render(request, 'profile_bookshelf.html', {'rec_books': rec_books})


def profile_edit(request):
    user = MongoUser.objects(id=_id).first()
    data = {
        'firstname': user.first_name,
        'lastname': user.last_name,
        'email': user.email,
        'login': user.username,
    }
    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        if form.is_valid():
            firstname = form.cleaned_data.get('firstname')
            lastname = form.cleaned_data.get('lastname')
            email = form.cleaned_data.get('email')
            login = form.cleaned_data.get('login')
            user.update(
                first_name=firstname,
                last_name=lastname,
                email=email,
                username=login
            )
            return redirect(profile_details)
    else:
        form = EditProfileForm(initial=data)
    return render(request, 'profile_edit.html', {'user': user, 'form': form})


def change_password(request):
    user = MongoUser.objects(id=_id).first()
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
    book = Book.objects(id=book_id).first()
    reviews = Review.objects(book_id=book_id)
    return render(request, 'book-details.html', {'book': book, 'reviews': reviews, 'user': None})


def add_review(request, user_id, book_id, text, rating):
    user = MongoUser.objects(id=user_id).first()
    book = Book.objects(id=book_id).first()
    review = Review(user_id=user.pk, book_id=book.pk, firstname=user.firstname, lastname=user.lastname, comment=text,
                    rating=rating)
    review.save()
    reviews = Review.objects(book_id=book_id)
    return render(request, 'book-details.html', {'book': book, 'reviews': reviews, 'user': user})

def change_review_status(request, book_id, user_id, review_id, new_status):
    review = Review.objects(id=review_id).first()
    user = MongoUser.objects(id=user_id).first()
    book = Book.objects(id=book_id).first()
    reviews = Review.objects(book_id=book_id)
    if review:
        review.update(status=new_status)
    return render(request, 'book-details.html', {'book': book, 'reviews': reviews, 'user': user})


def home(request):
    top_books = Book.objects.filter(statistic__rating__gte=4.5)[:10]
    new_books = Book.objects.order_by('-id')[:10]
    genres = []
    for genres_lst in Book.objects.values_list('genres'):
        for genre in genres_lst:
            if not genre in genres:
                genres.append(genre)
    return render(request, 'home.html', {'top_books': top_books, 'new_books': new_books, 'genres': genres})


def search_by_author(request, author_name):
    author = Author.objects(name=author_name)[0]
    books = [Book.objects(id=book_id)[0] for book_id in author.books]
    return render(request, 'books.html', {'books': books})


def category_search(request, genre):
    books = Book.objects.filter(genres=genre)
    return render(request, 'books.html', {'books': books})


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = MongoUser(email=form.cleaned_data.get('email'))
            user.first_name = form.cleaned_data.get('firstname')
            user.last_name = form.cleaned_data.get('lastname')
            user.username = form.cleaned_data.get('login')
            user.password = form.cleaned_data.get('password')
            user.save()

            return redirect(home)
    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})


def unique_registration_check(request, field_value):
    user = MongoUser.objects(Q(username=field_value) | Q(email=field_value))
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


def func_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request=request, username=username, password=password)
        if user:
            login(request, user)
            return HttpResponse(json.dumps({"message": "Success"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"message": "Denied"}), content_type="application/json")


@login_required
def profile_details(request):
    return render(request, 'profile_details.html')


@login_required
def profile_edit(request):
    return render(request, 'profile_edit.html')


def login_redirect_page(request):
    return render(request, 'login_redirect.html')
