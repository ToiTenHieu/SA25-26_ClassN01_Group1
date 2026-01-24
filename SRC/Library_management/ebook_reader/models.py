from django.db import models
from cloudinary.models import CloudinaryField
from Librarian.models import Book
class Ebook(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name='ebook')
    file = CloudinaryField(
        'ebooks',
        resource_type='raw',
    type='upload'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Ebook for '{self.book.title}'"