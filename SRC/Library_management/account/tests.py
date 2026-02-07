from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date, timedelta
from account.models import UserProfile
from account.membership_states import BasicState, StandardState, PremiumState
from Librarian.models import Book, BorrowRecord


class UserProfileModelTest(TestCase):
    """Unit tests for UserProfile model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            name='Test User',
            phone='0123456789',
            gender='male',
            membership_level='basic'
        )

    def test_user_profile_creation(self):
        """Test UserProfile can be created"""
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.name, 'Test User')
        self.assertEqual(self.profile.membership_level, 'basic')

    def test_get_membership_state_basic(self):
        """Test BasicState is returned for basic membership"""
        state = self.profile.get_membership_state()
        self.assertIsInstance(state, BasicState)
        self.assertEqual(state.max_books, 10)
        self.assertEqual(state.max_days, 14)
        self.assertEqual(state.free_extend, 0)
        self.assertFalse(state.has_priority())

    def test_get_membership_state_standard(self):
        """Test StandardState is returned for standard membership"""
        self.profile.membership_level = 'standard'
        self.profile.save()
        state = self.profile.get_membership_state()
        self.assertIsInstance(state, StandardState)
        self.assertEqual(state.max_books, 20)
        self.assertEqual(state.max_days, 30)
        self.assertEqual(state.free_extend, 2)
        self.assertTrue(state.has_priority())

    def test_get_membership_state_premium(self):
        """Test PremiumState is returned for premium membership"""
        self.profile.membership_level = 'premium'
        self.profile.save()
        state = self.profile.get_membership_state()
        self.assertIsInstance(state, PremiumState)
        self.assertEqual(state.max_books, 50)
        self.assertEqual(state.max_days, 60)
        self.assertEqual(state.free_extend, 5)
        self.assertTrue(state.has_priority())

    def test_max_books_property(self):
        """Test max_books property returns correct value"""
        self.assertEqual(self.profile.max_books, 10)
        self.profile.membership_level = 'premium'
        self.profile.save()
        self.assertEqual(self.profile.max_books, 50)

    def test_max_days_property(self):
        """Test max_days property returns correct value"""
        self.assertEqual(self.profile.max_days, 14)
        self.profile.membership_level = 'standard'
        self.profile.save()
        self.assertEqual(self.profile.max_days, 30)

    def test_upgrade_membership(self):
        """Test membership upgrade functionality"""
        self.assertEqual(self.profile.membership_level, 'basic')
        result = self.profile.upgrade_membership('premium')
        self.assertTrue(result)
        self.assertEqual(self.profile.membership_level, 'premium')

    def test_upgrade_membership_invalid(self):
        """Test upgrade with invalid level returns False"""
        result = self.profile.upgrade_membership('invalid')
        self.assertFalse(result)

    def test_total_renew_used(self):
        """Test total_renew_used calculates correctly"""
        book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            quantity=5
        )
        BorrowRecord.objects.create(
            user=self.profile,
            book=book,
            borrow_date=date.today(),
            due_date=date.today() + timedelta(days=14),
            status='borrowed',
            renew_count=2
        )
        BorrowRecord.objects.create(
            user=self.profile,
            book=book,
            borrow_date=date.today(),
            due_date=date.today() + timedelta(days=14),
            status='overdue',
            renew_count=1
        )
        total = self.profile.total_renew_used()
        self.assertEqual(total, 3)


class MembershipStateTest(TestCase):
    """Unit tests for MembershipState classes"""
    
    def test_basic_state(self):
        """Test BasicState properties"""
        state = BasicState()
        self.assertEqual(state.max_books, 10)
        self.assertEqual(state.max_days, 14)
        self.assertEqual(state.free_extend, 0)
        self.assertFalse(state.has_priority())

    def test_standard_state(self):
        """Test StandardState properties"""
        state = StandardState()
        self.assertEqual(state.max_books, 20)
        self.assertEqual(state.max_days, 30)
        self.assertEqual(state.free_extend, 2)
        self.assertTrue(state.has_priority())

    def test_premium_state(self):
        """Test PremiumState properties"""
        state = PremiumState()
        self.assertEqual(state.max_books, 50)
        self.assertEqual(state.max_days, 60)
        self.assertEqual(state.free_extend, 5)
        self.assertTrue(state.has_priority())


class AccountAPITest(TestCase):
    """API tests for Account views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            name='Test User',
            gender='male',
            membership_level='basic'
        )

    def test_register_api(self):
        """Test user registration API"""
        url = reverse('account:register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'confirm_password': 'newpass123',
            'name': 'New User',
            'phone': '0987654321',
            'gender': 'female'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_api(self):
        """Test login API"""
        url = reverse('account:login')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after login

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        url = reverse('account:login')
        data = {
            'username': 'testuser',
            'password': 'wrongpass'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)  # Stay on login page

    def test_profile_view_requires_login(self):
        """Test profile view requires authentication"""
        url = reverse('account:profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_profile_view_authenticated(self):
        """Test profile view for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('account:profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test User')

    def test_logout_api(self):
        """Test logout API"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('account:logout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)  # Redirect after logout
