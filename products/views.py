# views.py
from rest_framework import generics, status
from .models import Products, ProductVariant
from .serializers import (
    ProductVarianterializer,
    ProductCreateWithVariantsSerializer,
)
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import transaction
from .utils import restructure_product_creation_data


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Products.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProductCreateWithVariantsSerializer


    def post(self, request, *args, **kwargs):
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
    serializer_class = ProductVarianterializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        product_id = self.kwargs.get("product_id")
        return ProductVariant.objects.filter(product__id=product_id)

    def post(self, request, *args, **kwargs):
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
