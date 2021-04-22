from django.http import HttpResponse
from django.shortcuts import redirect, render

from admin.models import Book
from .forms import RegistrationForm


def home(request):
    return HttpResponse('<h1>Home page</h1>')


def book_details(request, book_id):
    # book_id = '60610c2952cd4157727d8ee3'
    book = Book.objects(id=book_id).first()
    return render(request, 'book-details.html', {'book': book})


def base(request):
    return render(request, 'base.html')


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            return redirect(home)

    else:
        form = RegistrationForm()

    return render(request, 'registration.html', {'form': form})
