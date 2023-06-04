from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from chain.models import Contact, Product, TradeUnit
from chain.serializers import ProductSerializer


# ----------------------------------------------------------------
# retail admin model
@admin.register(TradeUnit)
class RetailAdmin(admin.ModelAdmin):
    """
    Model representing retail admin panel

    Attrs:
        - list_display: defines collection of fields to display
        - list_filter: defines collection of fields to filter
        - actions: defines custom admin action
        - readonly_fields: defines collection with fields forbidden for editing
        - fieldsets: defines custom subsections
    """
    list_display = ('title', 'contact', 'products_', 'provider_', 'debt', 'unit_type', 'level')
    list_filter = ('contact__country', 'contact__city')
    actions = ['reset_debt']
    readonly_fields = ('level',)

    fieldsets = (
        ('Info', {
            'fields': ('title', 'unit_type', 'debt', 'level')
        }),
        ('Contact info', {
            'fields': ('contact',)
        }),
        ('Products', {
            'fields': ('products',)
        }),
        ('Provider', {
            'fields': ('provider',)
        })
    )

    def reset_debt(self, request, queryset) -> None:
        """Method to reset debt"""
        queryset.update(debt=0)

    @staticmethod
    def products_(obj):
        """
        Method to represent entity as a link
        """
        products = ProductSerializer(obj.products, many=True).data
        product_list = []
        for i, product in enumerate(products):
            product_url = reverse('admin:chain_product_change', args=[product['id']])
            product_link = format_html('<a href="{}">{}</a>', product_url, product['title'])
            product_list.append(f"{i + 1}. {product_link}")
        return format_html("<br>".join(product_list))

    def provider_(self, obj):
        """
        Method to represent entity as a link
        """
        if obj.provider:
            url = reverse('admin:chain_tradeunit_change', args=[obj.provider.id])
            return format_html('<a href="{}">{}</a>', url, obj.provider.title)
        return None

    provider_.short_description = 'Provider'


# ----------------------------------------------------------------
# contact admin model
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    """
    Model representing contact admin panel

    Attrs:
        - list_display: defines collection of fields to display
        - list_filter: defines collection of fields to filter
        - fieldsets: defines custom subsections
    """
    list_display = ('email', 'country', 'city', 'street', 'number')
    list_filter = ('country', 'city')

    fieldsets = (
        ('Info', {
            'fields': ('country', 'city', 'street', 'number')
        }),
        ('Email address', {
            'fields': ('email',)
        })
    )


# ----------------------------------------------------------------
# product admin model
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Model representing product admin panel

    Attrs:
        - list_display: defines collection of fields to display
        - list_filter: defines collection of fields to filter
        - fieldsets: defines custom subsections
    """
    list_display = ('title', 'model', 'release', 'price')
    list_filter = ('model',)

    fieldsets = (
        ('Info', {
            'fields': ('title', 'model')
        }),
        ('Price', {
            'fields': ('price',)
        }),
        ('Release date', {
            'fields': ('release',)
        })
    )

