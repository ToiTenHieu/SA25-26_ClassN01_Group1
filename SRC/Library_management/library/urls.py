from django.urls import path
from . import views

app_name='library'

urlpatterns = [
    path('catalog/', views.catalog, name='catalog'),
    path('home/', views.home, name='home'),
    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),
    path('membership/', views.membership, name='membership'),
    path('', views.home, name='home'),
    path('payment/', views.payment, name='payment'),
    path('process_payment/', views.process_payment, name='process_payment'),
    path('payment_done/', views.payment_done, name='payment_done'),
    path('digital/', views.digital, name='digital'),
    path('about/', views.about, name='about'),
    path('book-detail/<int:book_id>/', views.book_detail_view, name='book_detail_view'),
    path('borrow/', views.borrow_book, name='borrow_book'),  # ✅ Thêm dòng này
    path('borrowed_books/', views.borrowed_books, name='borrowed_books'),
    path('renew/<int:record_id>/', views.renew_book, name='renew_book'),
    path('extend_book/<int:record_id>/', views.extend_book, name='extend_book'),
    path('search/', views.search, name='search'),
    path('autocomplete/', views.autocomplete, name='autocomplete'),  # 👈 Thêm dòng này

]