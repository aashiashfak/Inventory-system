from django.contrib import admin
from .models import Products, VariantType, VariantOption, ProductVariant


@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    list_display = (
        "ProductName",
        "ProductCode",
        "ProductID",
        "CreatedUser",
        "TotalStock",
        "Active",
        "IsFavourite",
    )
    search_fields = ("ProductName", "ProductCode", "ProductID")
    list_filter = ("Active", "IsFavourite", "CreatedDate")
    readonly_fields = ("CreatedDate", "UpdatedDate")
    date_hierarchy = "CreatedDate"


@admin.register(VariantType)
class VariantTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(VariantOption)
class VariantOptionAdmin(admin.ModelAdmin):
    list_display = ("variant_type", "value")
    search_fields = ("value",)
    list_filter = ("variant_type",)


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ("product", "sku", "stock", "price")
    search_fields = ("sku", "product__ProductName")
    list_filter = ("product",)
    filter_horizontal = ("options",)
