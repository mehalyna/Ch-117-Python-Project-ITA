from django.http import HttpResponse
from django.shortcuts import redirect, render
from .forms import RegistrationForm
from .models import Book, User
from werkzeug.security import generate_password_hash


def profile_details(request):
    return render(request, 'profile_details.html')


def profile_edit(request):
    return render(request, 'profile_edit.html')


def change_password(request):
    return render(request, 'change_password.html')


def book_details(request, book_id):
    # book_id = '60610c2952cd4157727d8ee3'
    book = Book.objects(id=book_id).first()
    return render(request, 'book-details.html', {'book': book})


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
