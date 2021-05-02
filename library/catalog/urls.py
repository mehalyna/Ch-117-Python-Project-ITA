from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='library-home'),
    path('base/', views.base),
    path('registration/', views.registration, name='library-registration'),
    path('registration_validation/<str:field_value>', views.unique_registration_check, name='library-registration-validate'),
    path('book_details/<str:book_id>', views.book_details, name='book-details'),
    path('profile_details/', views.profile_details, name='profile_details'),
    path('profile_edit/', views.profile_edit, name='profile_edit'),
    path('change_password/', views.change_password, name='change_password'),
    path('books/<str:genre>/', views.category_search, name='library-books'),
    path('author_books/<str:author_name>/', views.search_by_author, name='library-books-author'),
    path('add_review/<str:user_id>/<str:book_id>/<str:text>', views.add_review, name='add-review'),
    path('add_rating/<str:user_id>/<str:book_id>/<int:rating>', views.add_rating, name='add-rating'),
    path('change_review_status/', views.change_review_status, name='change-review-status'),
    path('login/', views.login_view, name="my_login"),
    path('logout/', views.logout_view, name='my_logout'),
    path('profile_bookshelf/', views.profile_bookshelf, name='profile_bookshelf')

]
