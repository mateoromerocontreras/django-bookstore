from django.contrib import admin
from .models import Author, Editorial, Book, Cart, CartItem


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'nationality', 'birth_date', 'created_at']
    list_filter = ['nationality', 'created_at']
    search_fields = ['name', 'bio']
    ordering = ['name']


@admin.register(Editorial)
class EditorialAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'email', 'address']
    ordering = ['name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'isbn', 'author', 'editorial', 'seller', 'price', 'quantity', 'condition', 'is_available', 'created_at']
    list_filter = ['condition', 'is_available', 'language', 'created_at']
    search_fields = ['title', 'isbn', 'description']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username', 'user__email']
    ordering = ['-updated_at']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'book', 'quantity', 'created_at']
    list_filter = ['created_at']
    search_fields = ['book__title', 'cart__user__username']
    ordering = ['-created_at']
