from django.db.models.signals import pre_save
from django.dispatch import receiver

from chain.models import TradeUnit


# ----------------------------------------------------------------
@receiver(pre_save, sender=TradeUnit)
def set_tradeunit_level(sender, instance, **kwargs):
    """
    Called every time a TradeUnit is created to calculate the level in the hierarchy

    Raises:
        - ValueError (in case of trying to set provider to manufacture unit)
    """
    if instance.unit_type == TradeUnit.UnitType.manufacture:
        if instance.provider:
            raise ValueError('Manufacture should not have provider')
        instance.level = 0
    elif instance.provider.unit_type == TradeUnit.UnitType.manufacture:
        instance.level = 1
    else:
        instance.level = instance.provider.level + 1
