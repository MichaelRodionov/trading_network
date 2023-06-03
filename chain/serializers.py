from typing import Type, Any

from rest_framework import serializers

from chain.models import TradeUnit, Contact, Product


# ----------------------------------------------------------------
class ContactSerializer(serializers.ModelSerializer):
    """
    Contact serializer
    """
    class Meta:
        model: Type[Contact] = Contact
        fields: str = '__all__'


# ----------------------------------------------------------------
class ProductSerializer(serializers.ModelSerializer):
    """
    Product serializer
    """
    class Meta:
        model: Type[Product] = Product
        fields: str = '__all__'


# ----------------------------------------------------------------
class RetailCreateSerializer(serializers.ModelSerializer):
    """
    Retail create serializer

    Attrs:
        - provider: PrimaryKeyRelatedField defines related provider
        - contact: ContactSerializer handles incoming data with contact info
        - products: PrimaryKeyRelatedField defines related products
        - debt: DecimalField needed to define amount of debt between retailer and his provider
    """
    provider = serializers.PrimaryKeyRelatedField(queryset=TradeUnit.objects.all())
    contact = ContactSerializer()
    products = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True)
    debt = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)

    def create(self, validated_data) -> Type[TradeUnit]:
        """
        Redefined function to create a new trade unit (Create Contact entity and relates it with unit)

        Params:
            - validated_data: dictionary with validated data of TradeUnit entity

        Returns:
            TradeUnit object
        """
        contact_data, product_data = validated_data.pop('contact'), validated_data.pop('products')
        contact_serializer = ContactSerializer(data=contact_data)
        contact_serializer.is_valid(raise_exception=True)
        contact = contact_serializer.save()
        trade_unit = TradeUnit.objects.create(contact=contact, **validated_data)
        trade_unit.products.set(product_data)
        trade_unit.debt = sum([product.price for product in trade_unit.products.all()])
        trade_unit.save()
        return trade_unit

    class Meta:
        model: Type[TradeUnit] = TradeUnit
        exclude: list = ['level']


# ----------------------------------------------------------------
class RetailSerializer(serializers.ModelSerializer):
    """
    Retail serializer for list, retrieve, put, patch, destroy actions

    Attrs:
        - provider: SerializerMethodField defines recursive traversal of nested entities
        - contact: ContactSerializer handles data with contact info
        - products: ProductSerializer handles data with contact info
        - unit_type: SerializerMethodField defines readable information about unit type
    """
    provider = serializers.SerializerMethodField(required=False)
    contact = ContactSerializer(required=False)
    products = ProductSerializer(many=True, required=False)
    unit_type = serializers.SerializerMethodField(required=False)

    def get_unit_type(self, obj) -> Any:
        """
        Method to get readable information about unit type
        """
        return obj.get_unit_type_display()

    def get_provider(self, obj):
        """
        Method defines recursive traversal of nested entities
        """
        if obj.provider:
            provider_serializer = self.__class__(obj.provider)
            return provider_serializer.data
        return None

    class Meta:
        model: Type[TradeUnit] = TradeUnit
        exclude: list = ['level']
        read_only_fields: list = ['debt']
