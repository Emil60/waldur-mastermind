from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

PRICE_MAX_DIGITS = 22

PRICE_DECIMAL_PLACES = 10


class UnitPriceMixin(models.Model):
    """
    Mixin to expose standardized "unit_price" and "unit" field.
    """

    class Meta:
        abstract = True

    class Units:
        PER_MONTH = 'month'
        PER_HALF_MONTH = 'half_month'
        PER_DAY = 'day'
        PER_HOUR = 'hour'
        QUANTITY = 'quantity'

        CHOICES = (
            (PER_MONTH, _('Per month')),
            (PER_HALF_MONTH, _('Per half month')),
            (PER_DAY, _('Per day')),
            (PER_HOUR, _('Per hour')),
            (QUANTITY, _('Quantity')),
        )

    unit_price = models.DecimalField(
        default=0,
        max_digits=22,
        decimal_places=7,
        validators=[MinValueValidator(Decimal('0'))],
    )
    unit = models.CharField(default=Units.PER_DAY, max_length=30, choices=Units.CHOICES)


class ProductCodeMixin(models.Model):
    class Meta:
        abstract = True

    # article code is used for encoding product category in accounting software
    article_code = models.CharField(max_length=30, blank=True)


class BackendMetadataMixin(models.Model):
    class Meta:
        abstract = True

    backend_metadata = models.JSONField(
        default=dict,
        blank=True,
    )
