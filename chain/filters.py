from typing import Type

from django_filters import rest_framework as filters

from chain.models import TradeUnit


# ----------------------------------------------------------------
# custom filterset class
class RetailCountryFilter(filters.FilterSet):
    """
    Filterset class defining filter field
    """
    city = filters.CharFilter(field_name='contact__city')

    class Meta:
        model: Type[TradeUnit] = TradeUnit
        fields: list = ['city']
