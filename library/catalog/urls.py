from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='library-home'),
    path('base/', views.base),
    path('registration/', views.registration, name='library-registration'),
    path('registration_validation/<str:field_value>', views.unique_registration_check,
         name='library-registration-validate'),
    path('book_details/<str:book_id>', views.book_details, name='book-details'),
]
