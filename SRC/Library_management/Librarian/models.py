from django.db import models
from django.contrib.auth.models import User
from account.models import UserProfile
from datetime import date
from cloudinary.models import CloudinaryField
# Create your models here.
class Book(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),
    ]

    book_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    year = models.IntegerField(blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    description = models.TextField(blank=True, null=True)
    cover_image = CloudinaryField('image', folder='book_covers', blank=True, null=True)
    def __str__(self):
        return f"{self.title} - {self.author}"
from datetime import date, timedelta
from django.db import models
from .models import UserProfile, Book  # chỉnh lại import cho phù hợp

from datetime import timedelta, date

class BorrowRecord(models.Model):
    STATUS_CHOICES = [
        ('borrowed', 'Đang mượn'),
        ('returned', 'Đã trả'),
        ('overdue', 'Quá hạn'),
    ]

    record_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="borrow_records")
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrow_records")

    borrow_date = models.DateField()   # ngày mượn
    due_date = models.DateField()      # hạn trả
    return_date = models.DateField(blank=True, null=True)  # ngày trả
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='borrowed')

    renew_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Record {self.record_id} - {self.user} - {self.book}"

    @property
    def is_returned_late(self):
        if self.return_date and self.return_date > self.due_date:
            return True
        return False
    @property
    def days_left(self):
        """Số ngày còn lại trước hạn trả"""
        if self.status == 'borrowed' and self.due_date:
            return (self.due_date - date.today()).days
        return None
    @property
    def late_days(self):
        if self.return_date and self.due_date:
            delay = (self.return_date - self.due_date).days
            return delay if delay > 0 else 0
        elif self.status == 'overdue' and self.due_date:
            delay = (date.today() - self.due_date).days
            return delay if delay > 0 else 0
        return 0

    # ========== 🟢 Logic gia hạn ==========
    def can_extend(self):
        """Kiểm tra xem người dùng có thể gia hạn không."""
        state = self.user.get_membership_state()

        if state.free_extend is None:  # Gói cao cấp: không giới hạn
            return True
        return self.renew_count < state.free_extend

    def extend_due_date(self):
        """Gia hạn thêm 7 ngày nếu đủ điều kiện."""
        state = self.user.get_membership_state()

        if state.free_extend is None or self.renew_count < state.free_extend:
            self.due_date += timedelta(days=7)
            self.renew_count += 1

            # 🟡 Nếu sách đang quá hạn, đổi lại thành "borrowed"
            if self.status == 'overdue':
                self.status = 'borrowed'

            self.save()
            return True

        # Nếu đã hết lượt gia hạn
        return False
