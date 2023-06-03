from django.core.validators import MinValueValidator
from django.db import models


# ----------------------------------------------------------------
# contact model
class Contact(models.Model):
    """
    Model representing a contact data

    Attrs:
        - email: defines email address
        - country: defines country
        - city: defines city
        - street: defines street
        - number: defines number of building
    """
    email = models.EmailField(
        unique=True,
        verbose_name='Email address'
    )
    country = models.CharField(
        max_length=50,
        null=True,
        verbose_name='Country'
    )
    city = models.CharField(
        max_length=50,
        null=True,
        verbose_name='City'
    )
    street = models.CharField(
        max_length=50,
        null=True,
        verbose_name='Street'
    )
    number = models.CharField(
        max_length=10,
        null=True,
        verbose_name='Number of building'
    )

    def __str__(self):
        return f'{self.country}, {self.city}, {self.street}, {self.number}'

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'


# ----------------------------------------------------------------
# product model
class Product(models.Model):
    """
    Model representing a product

    Attrs:
        - title: defines title of product
        - model: defines model of product
        - release: defines release date of product
        - price: defines price of product
    """
    title = models.CharField(
        max_length=25,
        verbose_name='Title',
    )
    model = models.CharField(
        max_length=25,
        verbose_name='Model'
    )
    release = models.DateField(
        null=True,
        verbose_name='Release date'
    )
    price = models.DecimalField(
        max_digits=15,
        default=0.00,
        validators=[MinValueValidator(0)],
        decimal_places=2,
        verbose_name='Price',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


# ----------------------------------------------------------------
# trade unit model
class TradeUnit(models.Model):
    """
    Model representing a trade unit

    Attrs:
        - title: defines title of unit
        - contact: defines related contact
        - products: defines related products
        - provider: defines related provider
        - unit_type: defines type of unit. Choose by class UnitType
        - debt: defines amount of debt
        - level: defines level in retail network hierarchy
    """
    class UnitType(models.IntegerChoices):
        manufacture = 1, 'Factory'
        retail_network = 2, 'Retail Network'
        entrepreneur = 3, 'Individual entrepreneur'

    title = models.CharField(
        max_length=25,
        verbose_name='Title',
    )
    contact = models.ForeignKey(
        Contact,
        verbose_name='Contact',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    products = models.ManyToManyField(
        Product,
        related_name='units',
        verbose_name='Products',
        blank=True
    )
    provider = models.ForeignKey(
        'self',
        verbose_name='Provider',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    unit_type = models.PositiveSmallIntegerField(
        choices=UnitType.choices,
        default=UnitType.manufacture,
        verbose_name='Type of trade unit',
    )
    debt = models.DecimalField(
        max_digits=15,
        default=0.00,
        validators=[MinValueValidator(0)],
        decimal_places=2,
        verbose_name='Amount of debt',
        null=True,
        blank=True
    )
    level = models.IntegerField(
        default=0
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Trade unit'
        verbose_name_plural = 'Trade units'
