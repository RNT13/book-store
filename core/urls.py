"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.conf import settings
from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token


def home(request):
    return JsonResponse(
        {
            "message": "API Bookstore funcionando",
            "endpoints": {
                "admin": "/admin/",
                "__debug__": "/__debug__/",
                "orders": "/bookstore/v1/order/",
                "products": "/bookstore/v1/product/",
                "categories": "/bookstore/v1/product/categories/",
            },
        }
    )


urlpatterns = [
    path("", home),
    path("admin/", admin.site.urls),
    path("api-token-auth/", obtain_auth_token, name="api_token_auth"),
    path(
        "bookstore/<str:version>/",
        include(
            [
                path("order/", include("order.urls")),
                path("category/", include("product.urls")),
                path("product/", include("product.urls")),
            ]
        ),
    ),
]

# Incluir debug_toolbar somente se DEBUG=True
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
