from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='library-home'),
    path('registration/', views.registration, name='library-registation'),
]
