# ebook_reader/urls.py
from django.urls import path
from . import views

app_name = 'ebook_reader'

urlpatterns = [
    path('read/<int:ebook_id>/', views.read_ebook_view, name='read_ebook'),
    path('digital/',views.digital,name='digital'),
]