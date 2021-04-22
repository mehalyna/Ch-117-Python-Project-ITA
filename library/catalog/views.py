from django.http import HttpResponse
from django.shortcuts import redirect, render

from catalog.forms import RegistrationForm


def home(request):
    return HttpResponse('<h1>Home page</h1>')



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
