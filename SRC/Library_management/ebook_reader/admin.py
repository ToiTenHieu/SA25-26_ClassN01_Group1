# ebook_reader/admin.py
from django.contrib import admin
from .models import Ebook

@admin.register(Ebook)
class EbookAdmin(admin.ModelAdmin):
    list_display = ('id', 'book_title', 'book_author', 'uploaded_at')

    def book_title(self, obj):
        return obj.book.title
    book_title.short_description = 'Tên sách'

    def book_author(self, obj):
        return obj.book.author
    book_author.short_description = 'Tác giả'
