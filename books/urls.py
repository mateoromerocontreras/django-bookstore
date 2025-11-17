from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, EditorialViewSet, BookViewSet, AuthViewSet, CartViewSet

router = DefaultRouter()
router.register(r'authors', AuthorViewSet, basename='author')
router.register(r'editorials', EditorialViewSet, basename='editorial')
router.register(r'books', BookViewSet, basename='book')
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'cart', CartViewSet, basename='cart')

urlpatterns = [
    path('', include(router.urls)),
]

