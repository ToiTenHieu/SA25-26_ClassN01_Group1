from django.db import models

# Create your models here.
# library/models.py (Thêm vào file models.py của ứng dụng)

from django.db import models
from django.contrib.auth.models import User
from Librarian.models import Book # Giả định Model Book nằm trong cùng file
from Librarian.models import BorrowRecord # Giả định Model Book nằm trong cùng file

# library/models.py (Thêm vào cuối file)
from django.db.models import UniqueConstraint # Thêm import này

class Review(models.Model):
    RATING_CHOICES = [
        (1, '⭐'),
        (2, '⭐⭐'),
        (3, '⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (5, '⭐⭐⭐⭐⭐'),
    ]

    # Liên kết Khóa ngoại (Foreign Keys)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    # Sử dụng User model mặc định của Django
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    
    # Các trường đánh giá
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Đảm bảo mỗi người dùng chỉ được đánh giá một lần cho một cuốn sách
        unique_together = ('book', 'user') 
        # Tùy chọn: Sắp xếp đánh giá mới nhất lên đầu
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.user.username} for {self.book.title} ({self.rating} stars)"
# python manage.py makemigrations
# python manage.py migrate