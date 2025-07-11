# urls.py
from django.urls import path
from .views import (
    ProductListCreateAPIView,
    ProductVariantCreateAPIView
)

urlpatterns = [
    path(
        "list-create/", ProductListCreateAPIView.as_view(), name="product-list-create"
    ),
    path(
        "create-varients/<uuid:product_id>/",
        ProductVariantCreateAPIView.as_view(),
        name="product-list-create",
    ),
]
