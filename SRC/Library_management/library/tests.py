from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date, timedelta
import json
from Librarian.models import Book, BorrowRecord
from account.models import UserProfile
from library.models import Review


class ReviewModelTest(TestCase):
    """Unit tests for Review model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            quantity=5
        )

    def test_review_creation(self):
        """Test Review can be created"""
        review = Review.objects.create(
            book=self.book,
            user=self.user,
            rating=5,
            comment='Great book!'
        )
        self.assertEqual(review.book, self.book)
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, 'Great book!')

    def test_review_unique_together(self):
        """Test that user can only review a book once"""
        Review.objects.create(
            book=self.book,
            user=self.user,
            rating=5
        )
        # Try to create another review for same book and user
        review2, created = Review.objects.get_or_create(
            book=self.book,
            user=self.user,
            defaults={'rating': 4}
        )
        # Should get existing review, not create new one
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(review2.rating, 5)  # Original rating

    def test_review_str(self):
        """Test Review string representation"""
        review = Review.objects.create(
            book=self.book,
            user=self.user,
            rating=5
        )
        expected_str = f"Review by {self.user.username} for {self.book.title} (5 stars)"
        self.assertEqual(str(review), expected_str)


class LibraryAPITest(TestCase):
    """API tests for Library views"""
    
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

    def test_catalog_view(self):
        """Test catalog view"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('library:catalog')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Book')

    def test_search_api(self):
        """Test search functionality"""
        url = reverse('library:search')
        response = self.client.get(url, {'q': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Book')

    def test_autocomplete_api(self):
        """Test autocomplete API"""
        url = reverse('library:autocomplete')
        response = self.client.get(url, {'q': 'Test'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('results', data)

    def test_book_detail_view(self):
        """Test book detail view"""
        url = reverse('library:book_detail_view', args=[self.book.book_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Book')

    def test_borrow_book_api(self):
        """Test borrow book API"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('library:borrow_book')
        data = {
            'book_id': self.book.book_id,
            'borrow_date': str(date.today()),
            'return_date': str(date.today() + timedelta(days=14)),
            'quantity': 1
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        self.assertTrue(BorrowRecord.objects.filter(user=self.profile).exists())

    def test_borrow_book_exceeds_max_books(self):
        """Test borrow book when exceeding max books limit"""
        self.profile.membership_level = 'basic'
        self.profile.save()
        # Create 10 records to reach limit
        for i in range(10):
            book = Book.objects.create(
                title=f'Book {i}',
                author='Author',
                quantity=1
            )
            BorrowRecord.objects.create(
                user=self.profile,
                book=book,
                borrow_date=date.today(),
                due_date=date.today() + timedelta(days=14),
                status='borrowed'
            )
        
        self.client.login(username='testuser', password='testpass123')
        url = reverse('library:borrow_book')
        data = {
            'book_id': self.book.book_id,
            'borrow_date': str(date.today()),
            'return_date': str(date.today() + timedelta(days=14)),
            'quantity': 1
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        response_data = json.loads(response.content)
        self.assertFalse(response_data['success'])

    def test_borrow_book_already_borrowed(self):
        """Test borrow book when already borrowed"""
        BorrowRecord.objects.create(
            user=self.profile,
            book=self.book,
            borrow_date=date.today(),
            due_date=date.today() + timedelta(days=14),
            status='borrowed'
        )
        self.client.login(username='testuser', password='testpass123')
        url = reverse('library:borrow_book')
        data = {
            'book_id': self.book.book_id,
            'borrow_date': str(date.today()),
            'return_date': str(date.today() + timedelta(days=14)),
            'quantity': 1
        }
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        response_data = json.loads(response.content)
        self.assertFalse(response_data['success'])

    def test_review_submission(self):
        """Test review submission"""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('library:book_detail_view', args=[self.book.book_id])
        data = {
            'rating': 5,
            'comment': 'Excellent book!'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(
            Review.objects.filter(book=self.book, user=self.user).exists()
        )

    def test_borrowed_books_view(self):
        """Test borrowed books view"""
        BorrowRecord.objects.create(
            user=self.profile,
            book=self.book,
            borrow_date=date.today(),
            due_date=date.today() + timedelta(days=14),
            status='borrowed'
        )
        self.client.login(username='testuser', password='testpass123')
        url = reverse('library:borrowed_books')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Book')

    def test_renew_book_api(self):
        """Test renew book API"""
        record = BorrowRecord.objects.create(
            user=self.profile,
            book=self.book,
            borrow_date=date.today(),
            due_date=date.today() + timedelta(days=14),
            status='borrowed',
            renew_count=0
        )
        self.profile.membership_level = 'standard'
        self.profile.save()
        self.client.login(username='testuser', password='testpass123')
        url = reverse('library:renew_book', args=[record.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        record.refresh_from_db()
        self.assertEqual(record.renew_count, 1)
