from django.urls import path, include
from rest_framework.routers import DefaultRouter

from order import viewsets

router = DefaultRouter(trailing_slash=True)

router.register(r"order", viewsets.OrderViewSet, basename="order")

urlpatterns = [
    path("", include(router.urls)),
]
