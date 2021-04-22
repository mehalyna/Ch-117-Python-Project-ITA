from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='library-home'),
    path('base', views.base),
    path('registration/', views.registration, name='library-registration'),
]
