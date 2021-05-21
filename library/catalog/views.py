import json

from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from mongoengine.queryset.visitor import Q

from .forms import ChangePasswordForm, EditProfileForm, RegistrationForm
from .models import Author, Book, Review, MongoUser, Status


@login_required
def profile_details(request):
    return render(request, 'profile_details.html')


@login_required
def profile_edit(request):
    user = request.user.mongo_user
    data = {
        'user_id': user.id,
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
    return render(request, 'profile_edit.html', {'form': form})


@login_required
def change_password(request):
    user = request.user.mongo_user
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data.get('old_password')
            if user and user.check_password(old_password):
                new_password = form.cleaned_data.get('new_password')
                user.update(password=new_password)
                messages.success(request, 'Password successfully updated.')
                return redirect(profile_details)
            else:
                messages.error(request, 'Wrong old password.')
    else:
        form = ChangePasswordForm()
    return render(request, 'change_password.html', {'form': form})


@login_required
def profile_bookshelf(request):
    rec_books = sorted(Book.objects(status=Status.ACTIVE), key=lambda book: book.statistic.total_read, reverse=True)[:15]
    wishlist_books = []
    for book_id in request.user.mongo_user.wishlist:
        book = Book.objects(id=book_id).first()
        if book and book.status == Status.ACTIVE:
            wishlist_books.append(book)
    return render(request, 'profile_bookshelf.html', {'rec_books': rec_books, 'wishlist_books': wishlist_books})


@login_required
def add_to_wishlist(request, book_id):
    user = request.user.mongo_user
    book = Book.objects(Q(id=book_id) & Q(status=Status.ACTIVE)).first()
    if not book:
        return redirect(home)

    if not str(book_id) in user.wishlist:
        book = Book.objects(id=book_id).first()
        if book:
            book.update(statistic__total_read=book.statistic.total_read + 1)
            book.update(statistic__reading_now=book.statistic.reading_now + 1)
            user.wishlist.append(book_id)
            user.update(wishlist=user.wishlist)

    return redirect(book_details, book_id=book_id)


@login_required
def delete_from_wishlist(request, book_id):
    user = request.user.mongo_user
    book = Book.objects(Q(id=book_id) & Q(status=Status.ACTIVE)).first()
    if not book:
        return redirect(home)

    if str(book_id) in user.wishlist:
        book = Book.objects(id=book_id).first()
        book.update(statistic__reading_now=book.statistic.reading_now - 1)
        user.wishlist.remove(book_id)
        user.update(wishlist=user.wishlist)

    return redirect(book_details, book_id=book_id)


def book_details(request, book_id):
    if 'book_details' in request.META['HTTP_REFERER']:
        request.META['HTTP_REFERER'] = request.session['previous']
    else:
        request.session['previous'] = request.META['HTTP_REFERER']

    book = Book.objects(Q(id=book_id) & Q(status=Status.ACTIVE)).first()
    if not book:
        return redirect(home)

    reviews = Review.objects(book_id=book_id).order_by('-date')
    return render(request, 'book-details.html',
                  {'book': book, 'reviews': reviews, 'book_id': book_id})


@login_required
def add_review(request, book_id):
    text = request.GET.get('text-comment')
    if text.strip():
        book = Book.objects(Q(id=book_id) & Q(status=Status.ACTIVE)).first()
        if not book:
            return redirect(home)
        review = Review(user_id=request.user.mongo_user.pk, book_id=book.pk,
                        firstname=request.user.mongo_user.first_name,
                        lastname=request.user.mongo_user.last_name, comment=text)
        review.save()
    else:
        messages.error(request, "The comment field should not be blank")
    return redirect(book_details, book_id=book_id)


@login_required
def add_rating(request, book_id, rating=1):
    user = MongoUser.objects(id=request.user.mongo_user.id).first()
    user_rated_books = user.rated_books

    book = Book.objects(Q(id=book_id) & Q(status=Status.ACTIVE)).first()
    if not book:
        return redirect(home)

    if str(book_id) in user.rated_books.keys():
        book.statistic.stars[user.rated_books[str(book_id)] - 1] -= 1

    book.statistic.stars[rating - 1] += 1
    user_rated_books = dict(user_rated_books, **{str(book_id): rating - 1})
    user.update(rated_books=user_rated_books)
    book.save()
    book.calculate_rating()

    return HttpResponse('Success', content_type="text/plain")


@login_required
def change_review_status(request, book_id, review_id, new_status):
    review = Review.objects(id=review_id).first()
    if review:
        review.update(status=new_status)

    return redirect(book_details, book_id=book_id)


def home(request):
    top_books = sorted(Book.objects(status=Status.ACTIVE), key=lambda book: book.statistic.rating, reverse=True)[:20]
    new_books = Book.objects(status=Status.ACTIVE).order_by('-id')[:20]
    genres = []
    for genres_lst in Book.objects.values_list('genres'):
        for genre in genres_lst:
            if genre and genre not in genres:
                genres.append(genre)
    return render(request, 'home.html', {'top_books': top_books, 'new_books': new_books, 'genres': genres})


def information_page(request):
    return render(request, 'information_page.html')


def search_by_author(request, author_name):
    author = Author.objects(Q(name=author_name) & Q(status=Status.ACTIVE))[0]
    books = []
    for book_id in author.books:
        book = Book.objects(id=book_id)[0]
        if book and book.status == Status.ACTIVE:
            books.append(book)
    return render(request, 'books.html', {'books': books})


def category_search(request, genre):
    books = Book.objects.filter(Q(genres=genre) & Q(status=Status.ACTIVE))
    return render(request, 'books.html', {'books': books, 'genre': genre})


def form_search(request):
    q = request.GET.get('searchbar', '')
    if q:
        authors = Author.objects(Q(name__icontains=q) & Q(status=Status.ACTIVE))
        books_id = []
        for author in authors:
            for book_id in author.books:
                book = Book.objects(id=book_id)[0]
                if book and book.status == Status.ACTIVE:
                    books_id.append(book_id)
        books = Book.objects.filter(
            Q(status=Status.ACTIVE) & (Q(title__icontains=q) | Q(year__icontains=q) | Q(id__in=books_id)))
    else:
        return render(request, 'books.html')
    return render(request, 'books.html', {'books': books, 'q': q})


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('login')
            password = form.cleaned_data.get('password')

            MongoUser.objects.create_user(
                firstname=form.cleaned_data.get('firstname'),
                lastname=form.cleaned_data.get('lastname'),
                username=username,
                email=form.cleaned_data.get('email'),
                password=password,
            )

            user = authenticate(request=request, username=username, password=password)
            if user:
                login(request, user)

            script = f'''<script>
                            window.location.href = "{reverse(home)}";
                            localStorage.clear();
                        </script>'''

            return HttpResponse(script)
    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})


def unique_registration_check(request, field_value):
    user = MongoUser.objects(Q(username=field_value) | Q(email=field_value))
    if user:
        return HttpResponse('Already taken', content_type="text/plain")
    return HttpResponse('', content_type="text/plain")


def edit_profile_check(request, field_value):
    check_user = MongoUser.objects(Q(username=field_value) | Q(email=field_value)).first()
    username = request.user.mongo_user.username
    email = request.user.mongo_user.email
    if check_user.username != username or check_user.email != email:
        return HttpResponse('Already taken', content_type="text/plain")
    return HttpResponse('', content_type="text/plain")


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


def login_redirect_page(request):
    return render(request, 'login_redirect.html')


def news_page(request):
    return render(request, 'news_page.html')


def collections_page(request):
    pages_books = Book.objects(Q(pages__gte=1000) & Q(status=Status.ACTIVE))[:10]
    total_read_books = Book.objects(status=Status.ACTIVE).order_by('-statistic__total_read')[:10]
    return render(request, 'collections.html', {'pages_books': pages_books, 'total_read_books': total_read_books})


def authors_page(request):
    authors = Author.objects(status=Status.ACTIVE).order_by('name')
    return render(request, 'authors.html', {'authors': authors})
