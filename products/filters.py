import django_filters
from .models import StockReport


class StockReportFilter(django_filters.FilterSet):
    timestamp__gte = django_filters.DateFilter(
        field_name="timestamp", lookup_expr="gte"
    )
    timestamp__lte = django_filters.DateFilter(
        field_name="timestamp", lookup_expr="lte"
    )
    change_type = django_filters.ChoiceFilter(choices=StockReport.CHANGE_TYPE_CHOICES)
    variant__product__ProductName = django_filters.CharFilter(lookup_expr="icontains")
    variant__sku = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = StockReport
        fields = []
