# views.py
from rest_framework import generics, status
from .models import Products
from .serializers import (
    ProductCreateSerializer,
    ProductDetailSerializer,
    ProductVarianterializer,
)
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import transaction



class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Products.objects.all()
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ProductCreateSerializer
        return ProductDetailSerializer


class ProductVariantCreateAPIView(generics.CreateAPIView):
    serializer_class = ProductVarianterializer
    permission_classes = [IsAuthenticated]

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
