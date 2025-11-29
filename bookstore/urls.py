"""bookstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.conf import settings


@ensure_csrf_cookie
def get_csrf_token(request):
    token = get_token(request)
    return JsonResponse({"csrfToken": token})


def health_check(request):
    """Health check endpoint for Render"""
    return JsonResponse(
        {
            "status": "ok",
            "debug": settings.DEBUG,
            "allowed_hosts": settings.ALLOWED_HOSTS,
            "cors_origins": settings.CORS_ALLOWED_ORIGINS,
            "csrf_origins": settings.CSRF_TRUSTED_ORIGINS,
        }
    )


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/csrf-token/", get_csrf_token, name="csrf-token"),
    path("api/", include("books.urls")),
    path("health/", health_check, name="health-check"),
]
