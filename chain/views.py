from typing import Type

from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from chain.filters import RetailCountryFilter
from chain.models import TradeUnit
from chain.serializers import RetailSerializer, RetailCreateSerializer


# ----------------------------------------------------------------
@extend_schema(tags=['Retail Network'])
@extend_schema_view(
    create=extend_schema(
        description="Create new Retail Network",
        summary="Add Retail Network"
    ),
    retrieve=extend_schema(
        description="Get one Retail Network",
        summary="Get Retail Network"
    ),
    list=extend_schema(
        description="Get list of Retail Networks",
        summary="Get all Retail Networks"
    ),
    update=extend_schema(
        description="Full update of Retail Network",
        summary="Update Retail Network"
    ),
    partial_update=extend_schema(
        description="Partial update of Retail Network",
        summary="Partial update Retail Network"
    ),
    destroy=extend_schema(
        description="Delete Retail Network",
        summary="Delete Retail Network"
    ),
)
class RetailViewSet(ModelViewSet):
    """
    ViewSet to handle GET, POST, PUT, PATCH, DELETE requests for TradeUnit entity

    Attrs:
        - queryset: defines queryset for TradeUnit
        - default_serializer: defines default serializer^ when no one is chosen in serializers dict
        - serializers: defines dict with serializers depends on incoming  action
        - permission_classes: defines permissions for this APIView
        - filter_backends: defines collection of filtering options for list action
        - filterset_class: defines filterset class
    """
    queryset = TradeUnit.objects.all()
    default_serializer = RetailSerializer
    serializers: dict = {
        'create': RetailCreateSerializer
    }
    permission_classes: list = [IsAuthenticated]
    filter_backends: list = [DjangoFilterBackend]
    filterset_class: list = RetailCountryFilter

    def get_serializer_class(self) -> Type[RetailSerializer | RetailCreateSerializer]:
        """
        Redefined method to get serializer class depends on action

        Returns:
            - default serializer (RetailSerializer)
            - RetailCreateSerializer if action is 'create'
        """
        return self.serializers.get(self.action, self.default_serializer)
