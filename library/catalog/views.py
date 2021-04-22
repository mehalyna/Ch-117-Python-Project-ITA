from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import RegistrationForm


def home(request):
    return render(request, 'home.html')

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
