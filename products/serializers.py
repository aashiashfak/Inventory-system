# serializers.py

from rest_framework import serializers
from .models import Products, ProductVariant, VariantOption , VariantType
from django.db.models import Sum

#  Used for creating products
class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = [
            "ProductID",
            "ProductCode",
            "ProductName",
            "ProductImage",
            "HSNCode",
            "TotalStock",
            "IsFavourite",
            "Active",
        ]

    def create(self, validated_data):
        validated_data["CreatedUser"] = self.context["request"].user
        return super().create(validated_data)


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

    def create(self, validated_data):
        option_data = validated_data.pop("option_data")
        product = self.context["product"]

        # Create the variant object
        variant = ProductVariant.objects.create(product=product, **validated_data)

        option_objs = []
        for item in option_data:
            variant_type_name = item.get("variant_type")
            value = item.get("value")

            # Create or retrieve VariantType
            variant_type, _ = VariantType.objects.get_or_create(name=variant_type_name)

            # Create or retrieve VariantOption
            option, _ = VariantOption.objects.get_or_create(
                variant_type=variant_type, value=value
            )

            option_objs.append(option)

        # Associate options to the variant
        variant.options.set(option_objs)
        product.TotalStock = product.variants.aggregate(total=Sum('stock'))['total'] or 0
        product.save(update_fields=["TotalStock"])


        return variant


#  Used for Detailed Product data
class ProductDetailSerializer(serializers.ModelSerializer):
    variants = ProductVarianterializer(many=True, read_only=True)
    CreatedUser = serializers.StringRelatedField()

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
            "CreatedUser",
            "CreatedDate",
            "variants",
        ]
