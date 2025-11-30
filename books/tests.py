from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from .models import Author, Editorial, Book, Cart, CartItem


class AuthorTests(TestCase):
    """Test Author endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.author = Author.objects.create(
            name='Test Author',
            bio='A test author',
            nationality='US'
        )
    
    def test_list_authors(self):
        """Test GET /api/authors/"""
        response = self.client.get('/api/authors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Authors don't have pagination (pagination_class = None)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Author')
    
    def test_create_author_authenticated(self):
        """Test POST /api/authors/ - authenticated user"""
        self.client.force_authenticate(user=self.user)
        data = {
            'name': 'New Author',
            'bio': 'Bio',
            'nationality': 'UK'
        }
        response = self.client.post('/api/authors/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'New Author')
    
    def test_create_author_unauthenticated(self):
        """Test POST /api/authors/ - unauthenticated user cannot create"""
        data = {'name': 'New Author', 'bio': 'Bio'}
        response = self.client.post('/api/authors/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_get_author_detail(self):
        """Test GET /api/authors/{id}/"""
        response = self.client.get(f'/api/authors/{self.author.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Author')
    
    def test_update_author(self):
        """Test PUT/PATCH /api/authors/{id}/"""
        self.client.force_authenticate(user=self.user)
        data = {'name': 'Updated Author'}
        response = self.client.patch(f'/api/authors/{self.author.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Author')
    
    def test_delete_author(self):
        """Test DELETE /api/authors/{id}/"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/authors/{self.author.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Author.objects.filter(id=self.author.id).exists())


class EditorialTests(TestCase):
    """Test Editorial endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.editorial = Editorial.objects.create(
            name='Test Editorial',
            address='123 Main St',
            email='pub@example.com'
        )
    
    def test_list_editorials(self):
        """Test GET /api/editorials/"""
        response = self.client.get('/api/editorials/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Editorials don't have pagination (pagination_class = None)
        self.assertEqual(len(response.data), 1)
    
    def test_create_editorial_authenticated(self):
        """Test POST /api/editorials/"""
        self.client.force_authenticate(user=self.user)
        data = {'name': 'New Editorial', 'address': '456 Oak Ave'}
        response = self.client.post('/api/editorials/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class BookTests(TestCase):
    """Test Book endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='seller',
            email='seller@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='testpass123'
        )
        self.author = Author.objects.create(name='Author Name')
        self.editorial = Editorial.objects.create(name='Editorial Name')
        self.book = Book.objects.create(
            title='Test Book',
            isbn='9781234567890',
            price=Decimal('29.99'),
            author=self.author,
            editorial=self.editorial,
            seller=self.user,
            quantity=5
        )
    
    def test_list_books(self):
        """Test GET /api/books/"""
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Response is paginated
        self.assertIn('results', response.data)
        results = response.data['results']
        self.assertGreaterEqual(len(results), 1)
        # Verify the test book is in the list
        book_titles = [book['title'] for book in results]
        self.assertIn('Test Book', book_titles)
    
    def test_get_book_detail(self):
        """Test GET /api/books/{id}/"""
        response = self.client.get(f'/api/books/{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Book')
    
    def test_create_book_authenticated(self):
        """Test POST /api/books/"""
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New Book',
            'isbn': '9879879876543',
            'price': '39.99',
            'author_id': self.author.id,
            'editorial_id': self.editorial.id,
            'quantity': 3
        }
        response = self.client.post('/api/books/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['seller']['username'], 'seller')
    
    def test_create_book_unauthenticated(self):
        """Test POST /api/books/ - unauthenticated user cannot create"""
        data = {
            'title': 'New Book',
            'isbn': '9879879876543',
            'price': '39.99',
            'author_id': self.author.id,
            'editorial_id': self.editorial.id
        }
        response = self.client.post('/api/books/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_update_book_as_owner(self):
        """Test PATCH /api/books/{id}/ - owner can update"""
        self.client.force_authenticate(user=self.user)
        data = {'title': 'Updated Title', 'price': '49.99'}
        response = self.client.patch(f'/api/books/{self.book.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Title')
    
    def test_update_book_as_non_owner(self):
        """Test PATCH /api/books/{id}/ - non-owner cannot update"""
        self.client.force_authenticate(user=self.user2)
        data = {'title': 'Hacked Title'}
        response = self.client.patch(f'/api/books/{self.book.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_delete_book_as_owner(self):
        """Test DELETE /api/books/{id}/ - owner can delete"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/api/books/{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())
    
    def test_delete_book_as_non_owner(self):
        """Test DELETE /api/books/{id}/ - non-owner cannot delete"""
        self.client.force_authenticate(user=self.user2)
        response = self.client.delete(f'/api/books/{self.book.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class AuthenticationTests(TestCase):
    """Test Authentication endpoints"""
    
    def setUp(self):
        self.client = APIClient()
    
    def test_user_registration(self):
        """Test POST /api/auth/register/"""
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'securepass123',
            'first_name': 'John',
            'last_name': 'Doe'
        }
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'newuser')
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_registration_duplicate_username(self):
        """Test registration with duplicate username"""
        User.objects.create_user(username='testuser', email='test@example.com', password='pass')
        data = {
            'username': 'testuser',
            'email': 'another@example.com',
            'password': 'pass123'
        }
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('already exists', response.data['error'])
    
    def test_registration_missing_fields(self):
        """Test registration with missing required fields"""
        data = {'username': 'testuser'}  # Missing email and password
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_user_login(self):
        """Test POST /api/auth/login/"""
        User.objects.create_user(username='testuser', password='testpass123')
        data = {'username': 'testuser', 'password': 'testpass123'}
        response = self.client.post('/api/auth/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
    
    def test_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        User.objects.create_user(username='testuser', password='testpass123')
        data = {'username': 'testuser', 'password': 'wrongpass'}
        response = self.client.post('/api/auth/login/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_get_current_user(self):
        """Test GET /api/auth/user/"""
        user = User.objects.create_user(username='testuser', email='test@example.com')
        self.client.force_authenticate(user=user)
        response = self.client.get('/api/auth/user/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
    
    def test_get_user_unauthenticated(self):
        """Test GET /api/auth/user/ - unauthenticated fails"""
        response = self.client.get('/api/auth/user/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CartTests(TestCase):
    """Test Shopping Cart endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='buyer',
            email='buyer@example.com',
            password='testpass123'
        )
        self.author = Author.objects.create(name='Author')
        self.editorial = Editorial.objects.create(name='Editorial')
        self.seller = User.objects.create_user(username='seller', password='pass')
        self.book1 = Book.objects.create(
            title='Book 1',
            isbn='1111111111111',
            price=Decimal('29.99'),
            author=self.author,
            editorial=self.editorial,
            seller=self.seller,
            quantity=10
        )
        self.book2 = Book.objects.create(
            title='Book 2',
            isbn='2222222222222',
            price=Decimal('19.99'),
            author=self.author,
            editorial=self.editorial,
            seller=self.seller,
            quantity=5
        )
    
    def test_get_empty_cart(self):
        """Test GET /api/cart/"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/cart/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['items']), 0)
    
    def test_add_item_to_cart(self):
        """Test POST /api/cart/add_item/"""
        self.client.force_authenticate(user=self.user)
        data = {'book_id': self.book1.id, 'quantity': 2}
        response = self.client.post('/api/cart/add_item/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['quantity'], 2)
    
    def test_add_item_exceeds_stock(self):
        """Test adding more items than available"""
        self.client.force_authenticate(user=self.user)
        data = {'book_id': self.book1.id, 'quantity': 20}  # Only 10 available
        response = self.client.post('/api/cart/add_item/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('available', response.data['error'])
    
    def test_add_invalid_quantity(self):
        """Test adding item with invalid quantity"""
        self.client.force_authenticate(user=self.user)
        data = {'book_id': self.book1.id, 'quantity': 0}
        response = self.client.post('/api/cart/add_item/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_add_nonexistent_book(self):
        """Test adding nonexistent book"""
        self.client.force_authenticate(user=self.user)
        data = {'book_id': 9999, 'quantity': 1}
        response = self.client.post('/api/cart/add_item/', data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_update_cart_item(self):
        """Test PUT /api/cart/update_item/"""
        self.client.force_authenticate(user=self.user)
        # Add item first
        self.client.post('/api/cart/add_item/', {'book_id': self.book1.id, 'quantity': 2})
        # Update quantity
        data = {'book_id': self.book1.id, 'quantity': 5}
        response = self.client.put('/api/cart/update_item/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['quantity'], 5)
    
    def test_update_nonexistent_item(self):
        """Test updating item not in cart"""
        self.client.force_authenticate(user=self.user)
        data = {'book_id': self.book1.id, 'quantity': 5}
        response = self.client.put('/api/cart/update_item/', data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_remove_item_from_cart(self):
        """Test DELETE /api/cart/remove_item/"""
        self.client.force_authenticate(user=self.user)
        # Add item first
        self.client.post('/api/cart/add_item/', {'book_id': self.book1.id, 'quantity': 2})
        # Remove item
        response = self.client.delete(f'/api/cart/remove_item/?book_id={self.book1.id}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Verify removed
        cart_response = self.client.get('/api/cart/')
        self.assertEqual(len(cart_response.data['items']), 0)
    
    def test_clear_cart(self):
        """Test POST /api/cart/clear/"""
        self.client.force_authenticate(user=self.user)
        # Add items
        self.client.post('/api/cart/add_item/', {'book_id': self.book1.id, 'quantity': 2})
        self.client.post('/api/cart/add_item/', {'book_id': self.book2.id, 'quantity': 1})
        # Clear cart
        response = self.client.post('/api/cart/clear/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify cleared
        cart_response = self.client.get('/api/cart/')
        self.assertEqual(len(cart_response.data['items']), 0)
    
    def test_checkout_success(self):
        """Test POST /api/cart/checkout/"""
        self.client.force_authenticate(user=self.user)
        # Add items
        self.client.post('/api/cart/add_item/', {'book_id': self.book1.id, 'quantity': 2})
        self.client.post('/api/cart/add_item/', {'book_id': self.book2.id, 'quantity': 1})
        # Checkout
        response = self.client.post('/api/cart/checkout/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Checkout successful')
        self.assertEqual(len(response.data['purchased_items']), 2)
        # Verify inventory reduced
        self.book1.refresh_from_db()
        self.book2.refresh_from_db()
        self.assertEqual(self.book1.quantity, 8)  # 10 - 2
        self.assertEqual(self.book2.quantity, 4)  # 5 - 1
        # Verify cart cleared
        cart_response = self.client.get('/api/cart/')
        self.assertEqual(len(cart_response.data['items']), 0)
    
    def test_checkout_empty_cart(self):
        """Test checkout with empty cart"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post('/api/cart/checkout/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_checkout_insufficient_stock(self):
        """Test checkout when stock becomes insufficient"""
        self.client.force_authenticate(user=self.user)
        # Add more items than available
        self.client.post('/api/cart/add_item/', {'book_id': self.book2.id, 'quantity': 5})
        # Reduce stock manually to trigger error
        self.book2.quantity = 2
        self.book2.save()
        # Try checkout
        response = self.client.post('/api/cart/checkout/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_cart_requires_authentication(self):
        """Test that cart endpoints require authentication"""
        response = self.client.get('/api/cart/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        response = self.client.post('/api/cart/add_item/', {'book_id': 1, 'quantity': 1})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
