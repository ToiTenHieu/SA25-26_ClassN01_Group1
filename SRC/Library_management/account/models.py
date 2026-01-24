from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from .membership_states import BasicState, StandardState, PremiumState
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True, null=True)
    phone= models.CharField(max_length=15, blank=True)
    occupation = models.CharField(max_length=30, blank=True, null=True)
    date_of_birth = models.DateField(max_length=25, blank=True, null=True)
    address = models.TextField(max_length=100,blank=True,null=True)
    
    Gender_Choices = (
        ('male', 'Nam'),
        ('female', 'Nữ'),
        ('other', 'Khác')
    )
    gender = models.CharField(max_length=10,choices=Gender_Choices)

    Role_Choices = (
        ('user', 'user'),
        ('librarian', 'librarian'),
    )
    role = models.CharField(max_length=10, choices=Role_Choices, default='user')
    
    Membership_Choices=(
        ('basic','Cơ bản'),
        ('standard','Tiêu chuẩn'),
        ('premium','Cao cấp')
    )
    membership_level= models.CharField(max_length=15, choices=Membership_Choices, default='basic')

    membership_upgrade_date = models.DateField(blank=True, null=True, verbose_name="Ngày nâng cấp")
    membership_expiry_date = models.DateField(blank=True, null=True, verbose_name="Ngày hết hạn")
    
    # STATE Factory
    def get_membership_state(self):
        if self.membership_level == 'standard':
            return StandardState()
        elif self.membership_level == 'premium':
            return PremiumState()
        return BasicState()
        
    @property
    def max_books(self):
        return self.get_membership_state().max_books
    @property
    def max_days(self):
        return self.get_membership_state().max_days
    @property
    def free_extend(self):
        return self.get_membership_state().free_extend 
    def has_priority(self):
        return self.get_membership_state().has_priority()
    
    def upgrade_membership(self, new_level):
        levels = ['basic', 'standard', 'premium']
        if new_level not in levels:
            return False
        current_index = levels.index(self.membership_level)
        new_index = levels.index(new_level)
        if new_index > current_index:
            self.membership_level = new_level
            self.save()
            return True 
        return False
    def __str__(self):
        return self.name or self.user.username
    def get_full_name(self):
        return self.name or self.user.username or self.user.get_full_name()
    
    
    def total_renew_used(self):
        from django.apps import apps
        from django.db.models import Sum
        BorrowRecord = apps.get_model('Librarian', 'BorrowRecord')
        total = BorrowRecord.objects.filter(
            user=self,
            status__in=['borrowed', 'overdue']
        ).aggregate(total=Sum('renew_count'))['total'] or 0

        return total

        