from django.urls import path
from .views import CreateCheckoutSessionView, ProductLandingPageView

from . import views
urlpatterns = [
    path('home/', views.home, name='library-home'),
    path('registration/', views.registration, name='library-registration'),
    path('registration_unique_validation/', views.unique_registration_check,
         name='library-registration-validate'),
    path('edit_profile_unique_validation/', views.edit_profile_unique_check, name='edit-profile-validate'),
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
    path('show_reviews/<str:book_id>/', views.show_reviews, name='show_reviews'),
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
    path('reset_password/', views.reset_password, name='reset_password'),
    path('help/', views.help_email, name='help_email'),
    path('donate/', ProductLandingPageView.as_view(), name='donate-page'),
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('cancel/', views.donate_failed, name='donate_failed'),
    path('success/', views.donate_success, name='donate_success'),

]

