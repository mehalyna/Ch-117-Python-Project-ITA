import json
import random
import string

from bson import ObjectId
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from django.db.models import Q
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import ChangePasswordForm, EditProfileForm, RegistrationForm
from .models import Author, Book, Review, MongoUser, Status

PASSWORD_ITERATION = 5
MAX_PASSWORD_NUM = 22


@login_required
def profile_details(request):
    return render(request, 'profile_details.html')


@login_required
def profile_edit(request):
    user = request.user
    data = {
        'user_id': user.pk,
        'firstname': user.firstname,
        'lastname': user.lastname,
        'email': user.email,
        'username': user.username,
    }
    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        if form.is_valid():
            firstname = form.cleaned_data.get('firstname')
            lastname = form.cleaned_data.get('lastname')
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            MongoUser.objects.update(
                user=user,
                firstname=firstname,
                lastname=lastname,
                email=email,
                username=username
            )
            return redirect(profile_details)
    else:
        form = EditProfileForm(initial=data)
    return render(request, 'profile_edit.html', {'form': form})


@login_required
def change_password(request):
    user = request.user
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            old_password = form.cleaned_data.get('old_password')
            if user and user.check_password(old_password):
                new_password = form.cleaned_data.get('new_password')
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password successfully updated.')
                return redirect(profile_details)
            else:
                messages.error(request, 'Wrong old password.')
    else:
        form = ChangePasswordForm()
    return render(request, 'change_password.html', {'form': form})


@login_required
def profile_bookshelf(request):
    rec_books = Book.objects.filter(status=Status.ACTIVE).order_by('-statistic__total_read')[:15]
    wishlist_books = []
    for book_id in request.user.wishlist:
        book = Book.objects.filter(pk=ObjectId(book_id)).first()
        if book and book.status == Status.ACTIVE:
            wishlist_books.append(book)
    return render(request, 'profile_bookshelf.html', {'rec_books': rec_books, 'wishlist_books': wishlist_books})


@login_required
def add_to_wishlist(request, book_id):
    user = request.user
    book = Book.objects.filter(pk=ObjectId(book_id), status=Status.ACTIVE).first()
    if not book:
        return redirect(home)

    if not str(book_id) in user.wishlist:
        book = Book.objects.filter(pk=ObjectId(book_id)).first()
        if book:
            book.statistic.total_read = book.statistic.total_read + 1
            book.statistic.reading_now = book.statistic.reading_now + 1
            book.save()
            user.wishlist.append(book_id)
            user.save()

    return redirect(book_details, book_id=book_id)


@login_required
def delete_from_wishlist(request, book_id):
    user = request.user
    book = Book.objects.filter(pk=ObjectId(book_id), status=Status.ACTIVE).first()
    if not book:
        return redirect(home)

    if str(book_id) in user.wishlist:
        book = Book.objects.filter(pk=ObjectId(book_id)).first()
        book.statistic.reading_now = book.statistic.reading_now - 1
        user.wishlist.remove(book_id)
        user.save()

    return redirect(book_details, book_id=book_id)


def book_details(request, book_id):
    if 'book_details' in request.META['HTTP_REFERER']:
        request.META['HTTP_REFERER'] = request.session.get('previous') or reverse('library-home')
    else:
        request.session['previous'] = request.META['HTTP_REFERER']

    book = Book.objects.filter(pk=ObjectId(book_id), status=Status.ACTIVE).first()
    if not book:
        return redirect(home)

    reviews = Review.objects.filter(book_id=ObjectId(book_id)).order_by('-date')
    return render(request, 'book-details.html',
                  {'book': book, 'reviews': reviews, 'book_id': book_id})


def add_review(request, book_id):
    if not request.user.is_authenticated:
        return JsonResponse({"message": "Not authorized"})
    text = request.POST.get('text-comment')
    if text.strip():
        book = Book.objects.filter(pk=ObjectId(book_id), status=Status.ACTIVE).first()
        if not book:
            return redirect(home)
        review = Review(user=request.user,
                        book=book,
                        firstname=request.user.firstname,
                        lastname=request.user.lastname,
                        comment=text)
        review.save()
    else:
        messages.error(request, "The comment field should not be blank")
    reviews = serialize('json', Review.objects.filter(book_id=ObjectId(book_id)).order_by('-date'))
    return JsonResponse({"reviews": json.loads(reviews)})


def show_reviews(request, book_id):
    if not request.user.is_authenticated:
        return JsonResponse({"message": "Not authorized"})
    reviews = serialize('json', Review.objects.filter(book_id=ObjectId(book_id)).order_by('-date'))
    return JsonResponse({"reviews": json.loads(reviews)})


@login_required
def add_rating(request, book_id, rating=1):
    user = MongoUser.objects.filter(pk=request.user.pk).first()
    user_rated_books = user.rated_books

    book = Book.objects.filter(pk=ObjectId(book_id), status=Status.ACTIVE).first()
    if not book:
        return redirect(home)
    if str(book_id) in user.rated_books.keys():
        book.statistic.stars[user.rated_books[str(book_id)] - 1] -= 1

    book.statistic.stars[rating - 1] += 1
    user_rated_books = dict(user_rated_books, **{str(book_id): rating - 1})
    user.rated_books = user_rated_books
    user.save()
    book.calculate_rating()

    return HttpResponse('Success', content_type="text/plain")


@login_required
def change_review_status(request, book_id, review_id, new_status):
    review = Review.objects.filter(pk=ObjectId(review_id)).first()
    if review:
        review.status = new_status
        review.save()

    return HttpResponse('Success', content_type="text/plain")


def home(request):
    top_books = Book.objects.filter(status=Status.ACTIVE).order_by('-statistic__rating')[:20]
    new_books = Book.objects.filter(status=Status.ACTIVE).order_by('-pk')[:20]
    books_genres = []
    for genres_list in Book.objects.values('genres'):
        for genre in genres_list.get('genres'):
            if genre and genre not in books_genres:
                books_genres.append(genre)

    return render(request, 'home.html', {'top_books': top_books, 'new_books': new_books, 'genres': books_genres})


def information_page(request):
    return render(request, 'information_page.html')


def search_by_author(request, author_name):
    author = Author.objects.filter(name=author_name, status=Status.ACTIVE).first()
    books = []
    for book_id in author.books:
        book = Book.objects.filter(pk=ObjectId(book_id)).first()
        if book and book.status == Status.ACTIVE:
            books.append(book)
    return render(request, 'books.html', {'books': books})


def category_search(request, genre):
    books = Book.objects.filter(genres__contains=genre, status=Status.ACTIVE)
    return render(request, 'books.html', {'books': books, 'genre': genre})


def form_search(request):
    q = request.GET.get('searchbar', '')
    if q:
        authors = Author.objects.filter(name__icontains=q, status=Status.ACTIVE)
        books_id = []
        for author in authors:
            for book_id in author.books:
                book = Book.objects.filter(pk=ObjectId(book_id)).first()
                if book and book.status == Status.ACTIVE:
                    books_id.append(ObjectId(book_id))
        books = Book.objects.filter(
            Q(status=Status.ACTIVE) & (Q(title__icontains=q) | Q(year__icontains=q) | Q(pk__in=books_id)))
    else:
        return render(request, 'books.html')
    return render(request, 'books.html', {'books': books, 'q': q})


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
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


def unique_registration_check(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        field_value = data.get('field_value')
        user = MongoUser.objects.filter(Q(username=field_value) | Q(email=field_value)).first()
        if user:
            return JsonResponse({'error_message': 'Already taken'})

        return JsonResponse({})


def edit_profile_check(request, field_value):
    check_user = MongoUser.objects.filter(Q(username=field_value) | Q(email=field_value)).first()
    username = request.user.username
    email = request.user.email
    if check_user and (check_user.username != username or check_user.email != email):
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
    pages_books = Book.objects.filter(Q(pages__gte=1000) & Q(status=Status.ACTIVE))[:10]
    total_read_books = Book.objects.filter(status=Status.ACTIVE).order_by('-statistic__total_read')[:10]
    return render(request, 'collections.html', {'pages_books': pages_books, 'total_read_books': total_read_books})


def authors_page(request):
    authors = Author.objects.filter(status=Status.ACTIVE).order_by('name')
    return render(request, 'authors.html', {'authors': authors})


def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = MongoUser.objects.filter(email=email).first()
        if user:
            number_string = [str(i) for i in range(MAX_PASSWORD_NUM)]
            eng_alphabet = string.ascii_letters
            new_password = ''
            for i in range(PASSWORD_ITERATION):
                new_password += random.choice(eng_alphabet)
                new_password += random.choice(number_string)
            user.set_password(new_password)
            user.save()
            send_mail(
                'Library support',
                f'''
                Your temporary password - {new_password}
                You can authorize on home page
                Home page link - {request.build_absolute_uri(reverse(home))}
                ''',
                'pythonproject117@gmail.com',
                [email],
                fail_silently=False
            )
            messages.add_message(
                request,
                messages.SUCCESS,
                'Success! Check your email and sign in with new credentials.'
            )
        else:
            messages.add_message(
                request,
                messages.ERROR,
                'Warning! You entered the invalid email.'
            )
    return render(request, 'reset_password.html')
