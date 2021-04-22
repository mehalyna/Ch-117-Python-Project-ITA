from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def home(request):
    return HttpResponse('<h1>Home page</h1>')


def base(request):
    return render(request, 'base.html')
