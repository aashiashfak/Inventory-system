# views.py
from rest_framework import generics, status
from .models import Products, ProductVariant, StockReport
from .serializers import (
    ProductVarianterializer,
    ProductCreateWithVariantsSerializer,
    StockReportSerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import transaction
from .utils import restructure_product_creation_data
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from .filters import StockReportFilter


class ProductListCreateAPIView(generics.ListCreateAPIView):
    """
    API endpoint that allows products to be listed and created.
    """

    queryset = Products.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProductCreateWithVariantsSerializer

    def post(self, request, *args, **kwargs):
        """
        Create a new product with variants.
        """
        product_data = restructure_product_creation_data(request.data, request.FILES)
        print("Entered in post method")
        print("Product Data: ", product_data)
        serializer = self.get_serializer(data=product_data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()

        return Response(
            {"message": "Product created successfully", "product_id": product.id},
            status=status.HTTP_201_CREATED,
        )


class ProductVariantCreateAPIView(generics.ListCreateAPIView):
    """
    API endpoint that allows product variants to be listed and created.
    """

    serializer_class = ProductVarianterializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        product_id = self.kwargs.get("product_id")
        return (
            ProductVariant.objects.filter(product__id=product_id)
            .select_related("product", "product__CreatedUser")
            .prefetch_related("options__variant_type")
        )

    def post(self, request, *args, **kwargs):
        """
        Create a new product variant.
        """
        print("data", request.data)
        product_id = kwargs.get("product_id")
        try:
            product = Products.objects.get(pk=product_id)
        except Products.DoesNotExist:
            return Response({"detail": "Product not found."}, status=404)

        with transaction.atomic():
            serializer = self.get_serializer(
                data=request.data, context={"product": product}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateVariantStockAPIView(APIView):
    """
    API endpoint that allows to update the stock of a product variant with change_type.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        variant_id = kwargs.get("variant_id")
        change_type = request.data.get("change_type")
        amount = request.data.get("change_amount")
        change_amount = int(amount)

        errors = {}
        if not change_type:
            errors["change_type"] = ["This field is required."]
        if not change_amount:
            errors["change_amount"] = ["This field is required."]

        if errors:
            raise ValidationError(errors)

        try:
            variant = ProductVariant.objects.select_related("product").get(
                id=variant_id
            )
        except ProductVariant.DoesNotExist:
            return Response(
                {"detail": "Variant not found"}, status=status.HTTP_404_NOT_FOUND
            )

        old_stock = variant.stock

        if change_type == "purchase":
            new_stock = old_stock + change_amount
        elif change_type == "sale":
            if change_amount > old_stock:
                raise ValidationError(
                    {"change_amount": "Cannot sell more than current stock"}
                )
            new_stock = old_stock - change_amount

        with transaction.atomic():
            variant.stock = new_stock
            variant.save(update_fields=["stock"])

            product = variant.product
            product.TotalStock = sum(v.stock for v in product.variants.all())
            product.save(update_fields=["TotalStock"])

            StockReport.objects.create(
                variant=variant,
                changed_by=request.user,
                change_type=change_type,
                old_stock=old_stock,
                new_stock=new_stock,
                change_amount=change_amount,
            )

        return Response(
            {
                "message": "Stock updated successfully",
                "variant_id": variant.id,
                "old_stock": old_stock,
                "new_stock": new_stock,
            },
            status=status.HTTP_200_OK,
        )


class StockReportListView(generics.ListAPIView):
    """
    API endpoint to view stock reports.
    """

    queryset = StockReport.objects.select_related(
        "variant__product", "changed_by"
    ).all()
    serializer_class = StockReportSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = StockReportFilter
    ordering = ["-timestamp"]
