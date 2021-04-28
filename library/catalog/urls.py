from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='library-home'),
    path('base/', views.base),
    path('registration/', views.registration, name='library-registration'),
    path('book_details/<str:book_id>', views.book_details, name='book-details'),
    path('profile_details/', views.profile_details, name='profile_details'),
    path('profile_edit/', views.profile_edit, name='profile_edit'),
    path('change_password/', views.change_password, name='change_password'),
    path('login/', views.login_view, name="my_login"),
    path('logout/', views.logout_view, name='my_logout'),
    path('func_login', views.func_login, name='func_login')
]
