# serializers.py

from rest_framework import serializers
from .models import Products, ProductVariant, VariantOption, VariantType, StockReport
from django.db.models import Sum
from django.db import transaction
from rest_framework.exceptions import ValidationError


#  Variant Option Serializer
class VariantOptionSerializer(serializers.ModelSerializer):
    variant_type = serializers.StringRelatedField()

    class Meta:
        model = VariantOption
        fields = ["id", "variant_type", "value"]


# Productvariant serializer
class ProductVarianterializer(serializers.ModelSerializer):
    option_data = serializers.ListField(
        child=serializers.DictField(), write_only=True, required=True
    )
    options = VariantOptionSerializer(many=True, read_only=True)

    class Meta:
        model = ProductVariant
        fields = ["id", "sku", "stock", "price", "image", "option_data", "options"]


class ProductCreateWithVariantsSerializer(serializers.ModelSerializer):
    variants = ProductVarianterializer(many=True, required=True)

    class Meta:
        model = Products
        fields = [
            "id",
            "ProductID",
            "ProductCode",
            "ProductName",
            "ProductImage",
            "HSNCode",
            "TotalStock",
            "IsFavourite",
            "Active",
            "variants",
        ]

    def create(self, validated_data):
        variants_data = validated_data.pop("variants", [])
        validated_data["CreatedUser"] = self.context["request"].user

        with transaction.atomic():
            # Create product
            product = Products.objects.create(**validated_data)

            # Create variants
            total_stock = 0
            for variant_data in variants_data:
                option_data = variant_data.pop("option_data")

                sku = variant_data.get("sku")

                if ProductVariant.objects.filter(sku=sku).exists():
                    raise ValidationError(f"Variant SKU '{sku}' already exists.")

                variant = ProductVariant.objects.create(product=product, **variant_data)

                option_objs = []
                for item in option_data:
                    variant_type_name = item.get("variant_type")
                    value = item.get("value")

                    variant_type, _ = VariantType.objects.get_or_create(
                        name=variant_type_name
                    )
                    option, _ = VariantOption.objects.get_or_create(
                        variant_type=variant_type, value=value
                    )

                    option_objs.append(option)

                variant.options.set(option_objs)
                total_stock += variant.stock or 0

            product.TotalStock = total_stock
            product.save(update_fields=["TotalStock"])

        return product


class StockReportSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source="variant.product.ProductName", read_only=True
    )
    sku = serializers.CharField(source="variant.sku", read_only=True)
    price = serializers.DecimalField(
        source="variant.price", max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = StockReport
        fields = [
            "id",
            "product_name",
            "sku",
            "price",
            "change_type",
            "old_stock",
            "new_stock",
            "change_amount",
            "timestamp",
            "changed_by",
        ]
