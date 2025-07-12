import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from versatileimagefield.fields import VersatileImageField
from accounts.models import CustomUser

# Create your models here.
class Products(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ProductID = models.BigIntegerField(unique=True)
    ProductCode = models.CharField(max_length=255, unique=True)
    ProductName = models.CharField(max_length=255)
    ProductImage = VersatileImageField(upload_to="uploads/", blank=True, null=True)
    CreatedDate = models.DateTimeField(auto_now_add=True)
    UpdatedDate = models.DateTimeField(blank=True, null=True)
    CreatedUser = models.ForeignKey(
        CustomUser, related_name="user%(class)s_objects", on_delete=models.CASCADE
    )
    IsFavourite = models.BooleanField(default=False)
    Active = models.BooleanField(default=True)
    HSNCode = models.CharField(max_length=255, blank=True, null=True)
    TotalStock = models.DecimalField(
        default=0.00, max_digits=20, decimal_places=8, blank=True, null=True
    )

    class Meta:
        db_table = "products_product"
        verbose_name = _("product")
        verbose_name_plural = _("products")
        unique_together = (("ProductCode", "ProductID"),)
        ordering = ("-CreatedDate", "ProductID")


    def __str__(self):
        return self.ProductName


class VariantType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class VariantOption(models.Model):
    variant_type = models.ForeignKey(
        VariantType, on_delete=models.CASCADE, related_name="options"
    )
    value = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.variant_type.name}: {self.value}"


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Products, on_delete=models.CASCADE, related_name="variants"
    )

    sku = models.CharField(max_length=100, unique=True)
    stock = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    options = models.ManyToManyField(
        VariantOption, related_name="product_variants"
    )  
    image = VersatileImageField(
        upload_to="uploads/variant_images/", blank=True, null=True
    )
    def __str__(self):
        return f"{self.product.ProductName} - {self.sku}"
