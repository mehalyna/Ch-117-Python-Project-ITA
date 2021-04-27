from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='library-home'),
    path('base/', views.base),
    path('registration/', views.registration, name='library-registration'),
    path('registration_validation/<str:field_value>', views.unique_registration_check,
         name='library-registration-validate'),
    path('book_details/<str:book_id>', views.book_details, name='book-details'),
    path('profile_details/', views.profile_details, name='profile_details'),
    path('profile_edit/', views.profile_edit, name='profile_edit'),
    path('change_password/', views.change_password, name='change_password'),
]
