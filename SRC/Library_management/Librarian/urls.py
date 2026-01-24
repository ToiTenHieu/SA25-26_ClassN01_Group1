from django.urls import path
from . import views
app_name = 'librarian' 
urlpatterns = [
    path('users/<int:user_id>/edit/', views.edit_user, name='edit_user'),
    path("api/users/<int:user_id>/delete/", views.delete_user_api, name="delete_user_api"),
    path("api/add-book/", views.add_book, name="add_book"),
    path("add-book/", views.add_book, name="add_book"),
    path("api/books/", views.book_list, name="book_list"),
    path("api/books/<int:book_id>/", views.book_detail, name="book_detail"),
    path('managebook/', views.librarian_dashboard, name='managebook'),
    path('api/return-book/<int:record_id>/', views.return_book_api, name='return_book_api'),
]
