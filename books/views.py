from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import transaction
from decimal import Decimal
import logging
from .models import Author, Editorial, Book, Cart, CartItem
from .serializers import (
    AuthorSerializer, EditorialSerializer, BookSerializer,
    BookListSerializer, UserSerializer, CartSerializer, CartItemSerializer
)

logger = logging.getLogger(__name__)


class IsOwnerOrReadOnly(IsAuthenticatedOrReadOnly):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        # Write permissions are only allowed to the owner of the book
        return obj.seller == request.user


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None  # Disable pagination for authors (small dataset)


class EditorialViewSet(viewsets.ModelViewSet):
    queryset = Editorial.objects.all()
    serializer_class = EditorialSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None  # Disable pagination for editorials (small dataset)


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return BookListSerializer
        return BookSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrReadOnly()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class AuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def register(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')

        if not username or not email or not password:
            return Response(
                {'error': 'Username, email, and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'Username already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {'error': 'Email already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        logger.info(f"Login attempt for username: {username}")
        logger.info(f"  Remote address: {request.META.get('REMOTE_ADDR')}")
        logger.info(f"  Origin: {request.META.get('HTTP_ORIGIN')}")
        
        if not username or not password:
            logger.warning(f"Login failed: missing credentials")
            return Response(
                {'error': 'Username and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            logger.info(f"Login successful for {username}, session: {request.session.session_key}")
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            logger.warning(f"Login failed: invalid credentials for {username}")
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        logout(request)
        return Response({'message': 'Successfully logged out'})

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def user(self, request):
        logger.info(f"User endpoint accessed")
        logger.info(f"  Authenticated: {request.user.is_authenticated}")
        logger.info(f"  User: {request.user.username if request.user.is_authenticated else 'Anonymous'}")
        logger.info(f"  Session ID: {request.session.session_key}")
        logger.info(f"  Cookies in request: {list(request.COOKIES.keys())}")
        logger.info(f"  Auth: {request.META.get('HTTP_AUTHORIZATION')}")
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_cart(self, user):
        """Get or create cart for user"""
        cart, created = Cart.objects.get_or_create(user=user)
        return cart

    def list(self, request):
        """Get current user's cart"""
        cart = self.get_cart(request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add_item(self, request):
        """Add item to cart"""
        book_id = request.data.get('book_id')
        quantity = int(request.data.get('quantity', 1))

        if not book_id:
            return Response(
                {'error': 'book_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response(
                {'error': 'Book not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        if quantity <= 0:
            return Response(
                {'error': 'Quantity must be greater than 0'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if book.quantity < quantity:
            return Response(
                {'error': f'Only {book.quantity} copies available'},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart = self.get_cart(request.user)

        # Check if item already exists in cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            book=book,
            defaults={'quantity': quantity}
        )

        if not created:
            # Update quantity if item exists
            new_quantity = cart_item.quantity + quantity
            if new_quantity > book.quantity:
                return Response(
                    {'error': f'Cannot add {quantity} more. Only {book.quantity - cart_item.quantity} available'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            cart_item.quantity = new_quantity
            cart_item.save()

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)

    @action(detail=False, methods=['put', 'patch'])
    def update_item(self, request):
        """Update quantity of item in cart"""
        book_id = request.data.get('book_id')
        quantity = int(request.data.get('quantity', 1))

        if not book_id:
            return Response(
                {'error': 'book_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if quantity <= 0:
            return Response(
                {'error': 'Quantity must be greater than 0'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response(
                {'error': 'Book not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        cart = self.get_cart(request.user)

        try:
            cart_item = CartItem.objects.get(cart=cart, book=book)
        except CartItem.DoesNotExist:
            return Response(
                {'error': 'Item not found in cart'},
                status=status.HTTP_404_NOT_FOUND
            )

        if quantity > book.quantity:
            return Response(
                {'error': f'Only {book.quantity} copies available'},
                status=status.HTTP_400_BAD_REQUEST
            )

        cart_item.quantity = quantity
        cart_item.save()

        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)

    @action(detail=False, methods=['delete'])
    def remove_item(self, request):
        """Remove item from cart"""
        book_id = request.query_params.get('book_id') or request.data.get('book_id')

        if not book_id:
            return Response(
                {'error': 'book_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response(
                {'error': 'Book not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        cart = self.get_cart(request.user)

        try:
            cart_item = CartItem.objects.get(cart=cart, book=book)
            cart_item.delete()
            return Response({'message': 'Item removed from cart'}, status=status.HTTP_204_NO_CONTENT)
        except CartItem.DoesNotExist:
            return Response(
                {'error': 'Item not found in cart'},
                status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=False, methods=['post'])
    def clear(self, request):
        """Clear entire cart"""
        cart = self.get_cart(request.user)
        cart.items.all().delete()
        return Response({'message': 'Cart cleared'})

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        """Process checkout - reduce book quantities and clear cart"""
        cart = self.get_cart(request.user)

        if not cart.items.exists():
            return Response(
                {'error': 'Cart is empty'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate all items have sufficient quantity
        errors = []
        for item in cart.items.all():
            if item.quantity > item.book.quantity:
                errors.append(f'Not enough copies of "{item.book.title}". Available: {item.book.quantity}, Requested: {item.quantity}')

        if errors:
            return Response(
                {'errors': errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Process checkout
        purchased_items = []
        # Calculate total before clearing cart
        total = cart.get_total()
        
        try:
            with transaction.atomic():
                for item in cart.items.all():
                    # Reduce book quantity
                    item.book.quantity -= item.quantity
                    item.book.save()  # This will update is_available automatically

                    purchased_items.append({
                        'book': item.book.title,
                        'quantity': item.quantity,
                        'price': str(item.book.price),
                        'subtotal': str(item.get_subtotal())
                    })

                # Clear cart
                cart.items.all().delete()

            return Response({
                'message': 'Checkout successful',
                'purchased_items': purchased_items,
                'total': str(total)
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'error': f'Checkout failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
