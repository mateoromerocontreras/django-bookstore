from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Author, Editorial, Book, Cart, CartItem


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio', 'birth_date', 'nationality', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class EditorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Editorial
        fields = ['id', 'name', 'address', 'phone', 'email', 'website', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), source='author', write_only=True)
    editorial = EditorialSerializer(read_only=True)
    editorial_id = serializers.PrimaryKeyRelatedField(queryset=Editorial.objects.all(), source='editorial', write_only=True)
    seller = UserSerializer(read_only=True)
    seller_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='seller', write_only=True, required=False)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'isbn', 'description', 'publication_date', 'price',
            'condition', 'pages', 'language', 'author', 'author_id',
            'editorial', 'editorial_id', 'seller', 'seller_id',
            'quantity', 'is_available', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Set seller to current user if not provided
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            validated_data['seller'] = request.user
        return super().create(validated_data)


class BookListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list views"""
    author_name = serializers.CharField(source='author.name', read_only=True)
    editorial_name = serializers.CharField(source='editorial.name', read_only=True)
    seller_username = serializers.CharField(source='seller.username', read_only=True)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'isbn', 'price', 'condition', 'quantity', 'is_available',
            'author_name', 'editorial_name', 'seller_username', 'created_at'
        ]


class CartItemSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), source='book', write_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'book', 'book_id', 'quantity', 'subtotal', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_subtotal(self, obj):
        return obj.get_subtotal()


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

    def get_total(self, obj):
        return obj.get_total()

