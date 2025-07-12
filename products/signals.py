from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ProductVariant, StockReport


@receiver(post_save, sender=ProductVariant)
def log_initial_stock(sender, instance, created, **kwargs):
    if created and instance.stock > 0:
        StockReport.objects.create(
            variant=instance,
            changed_by=instance.product.CreatedUser,  
            change_type="purchase",
            old_stock=0,
            new_stock=instance.stock,
            change_amount=instance.stock,
        )
