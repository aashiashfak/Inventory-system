from datetime import datetime, time
import django_filters as filters
from pytz import timezone as pytz_timezone, UTC
from .models import StockReport

# Define your desired timezone (India Standard Time)
IST = pytz_timezone("Asia/Kolkata")


class StockReportFilter(filters.FilterSet):
    timestamp__gte = filters.DateFilter(method="filter_timestamp__gte")
    timestamp__lte = filters.DateFilter(method="filter_timestamp__lte")
    change_type = filters.ChoiceFilter(choices=StockReport.CHANGE_TYPE_CHOICES)
    variant__product__ProductName = filters.CharFilter(lookup_expr="icontains")
    variant__sku = filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = StockReport
        fields = []

    def filter_timestamp__gte(self, queryset, name, value):
        """
        Filters records from the start of the selected date in IST.
        """
        ist_start = IST.localize(datetime.combine(value, time.min))
        utc_start = ist_start.astimezone(UTC)
        return queryset.filter(timestamp__gte=utc_start)

    def filter_timestamp__lte(self, queryset, name, value):
        """
        Filters records up to the end of the selected date in IST.
        """
        ist_end = IST.localize(datetime.combine(value, time.max))
        utc_end = ist_end.astimezone(UTC)
        return queryset.filter(timestamp__lte=utc_end)
