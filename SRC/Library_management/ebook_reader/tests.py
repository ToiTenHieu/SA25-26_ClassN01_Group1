from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from Librarian.models import Book
from ebook_reader.models import Ebook
from account.models import UserProfile


class EbookModelTest(TestCase):
    """Unit tests for Ebook model"""
    
    def setUp(self):
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            quantity=5
        )

    def test_ebook_creation(self):
        """Test Ebook can be created"""
        # Note: CloudinaryField requires actual file upload in real scenario
        # This test checks the model structure
        ebook = Ebook.objects.create(
            book=self.book,
            file='test_file.pdf'  # In real scenario, this would be CloudinaryField
        )
        self.assertEqual(ebook.book, self.book)
        self.assertIsNotNone(ebook.uploaded_at)

    def test_ebook_str(self):
        """Test Ebook string representation"""
        ebook = Ebook.objects.create(
            book=self.book,
            file='test_file.pdf'
        )
        expected_str = f"Ebook for '{self.book.title}'"
        self.assertEqual(str(ebook), expected_str)

    def test_ebook_one_to_one_with_book(self):
        """Test Ebook has one-to-one relationship with Book"""
        ebook = Ebook.objects.create(
            book=self.book,
            file='test_file.pdf'
        )
        # Access ebook from book
        self.assertEqual(self.book.ebook, ebook)


class EbookReaderAPITest(TestCase):
    """API tests for Ebook Reader views"""
    
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
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            quantity=5
        )
        self.ebook = Ebook.objects.create(
            book=self.book,
            file='test_file.pdf'
        )

    def test_digital_view(self):
        """Test digital ebook listing view"""
        url = reverse('ebook_reader:digital')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_read_ebook_view(self):
        """Test read ebook view"""
        url = reverse('ebook_reader:read_ebook', args=[self.ebook.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.book.title)

    def test_read_ebook_view_not_found(self):
        """Test read ebook view with invalid ID"""
        url = reverse('ebook_reader:read_ebook', args=[99999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
