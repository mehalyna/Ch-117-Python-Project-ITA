from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('home/', views.home, name='library-home'),
    path('registration/', views.registration, name='library-registration'),
    path('registration_unique_validation/', views.unique_registration_check,
         name='library-registration-validate'),
    path('edit_profile_validation/<str:field_value>', views.edit_profile_check, name='library-edit-profile-validate'),
    path('book_details/<str:book_id>', views.book_details, name='book-details'),
    path('profile_details/', views.profile_details, name='profile_details'),
    path('profile_edit/', views.profile_edit, name='profile_edit'),
    path('change_password/', views.change_password, name='change_password'),
    path('search/', views.form_search, name='form-books'),
    path('books/<str:genre>/', views.category_search, name='library-books'),
    path('func_login', views.func_login, name='func_login'),
    path('login_redirect_page/', views.login_redirect_page, name='login_redirect_page'),
    path('logout/', views.logout_view, name='logout'),
    path('author_books/<str:author_name>/', views.search_by_author, name='library-books-author'),
    path('add_review/<str:book_id>/', views.add_review, name='add-review'),
    path('add_rating/<str:book_id>/', views.add_rating, name='add-rating'),
    path('add_rating/<str:book_id>/<int:rating>/', views.add_rating, name='add-rating'),
    path('add_to_wishlist/<str:book_id>/', views.add_to_wishlist, name='add-to-wishlist'),
    path('delete_from_wishlist/<str:book_id>/', views.delete_from_wishlist, name='delete-from-wishlist'),
    path('change_review_status/<str:book_id>/<str:review_id>/<str:new_status>/', views.change_review_status,
         name='change-review-status'),
    path('profile_bookshelf/', views.profile_bookshelf, name='profile_bookshelf'),
    path('information/', views.information_page, name='information_page'),
    path('news/', views.news_page, name='news_page'),
    path('collections/', views.collections_page, name='collections_page'),
    path('authors/', views.authors_page, name='authors_page'),

    # password recovery
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name='password_reset.html'),
         name='reset_password'),
    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_form.html'),
         name='password_reset_confirm'),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete'),
]
