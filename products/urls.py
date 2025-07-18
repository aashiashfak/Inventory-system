from django.urls import path
from .views import (
    ProductListCreateAPIView,
    ProductVariantCreateAPIView,
    UpdateVariantStockAPIView,
    StockReportListView,
)

urlpatterns = [
    path(
        "list-create/", ProductListCreateAPIView.as_view(), name="product-list-create"
    ),
    path(
        "varient-list-create/<uuid:product_id>/",
        ProductVariantCreateAPIView.as_view(),
        name="product-varient-list-create",
    ),
    path(
        "variant/<int:variant_id>/update-stock/",
        UpdateVariantStockAPIView.as_view(),
        name="update-variant-stock",
    ),
    path("varient/stock-reports/", StockReportListView.as_view(), name="stock-report-list"),
]
