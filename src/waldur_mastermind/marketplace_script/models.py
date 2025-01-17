from django.db import models
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from django_fsm import FSMIntegerField, transition
from model_utils.models import TimeStampedModel

from waldur_core.core import models as core_models
from waldur_mastermind.marketplace import models as marketplace_models


class DryRun(
    core_models.UuidMixin,
    core_models.ErrorMessageMixin,
    TimeStampedModel,
):
    class States:
        PENDING = 1
        EXECUTING = 2
        DONE = 3
        ERRED = 4

        CHOICES = (
            (PENDING, 'pending'),
            (EXECUTING, 'executing'),
            (DONE, 'done'),
            (ERRED, 'erred'),
        )

    order = models.ForeignKey(
        on_delete=models.SET_NULL,
        to=marketplace_models.Order,
        null=True,
    )
    order_item_attributes = models.JSONField(blank=True, default=dict)
    order_item_plan = models.ForeignKey(
        on_delete=models.CASCADE, to=marketplace_models.Plan
    )
    order_item_offering = models.ForeignKey(
        on_delete=models.SET_NULL, null=True, to=marketplace_models.Offering
    )
    order_item_type = models.CharField(max_length=255)
    state = FSMIntegerField(default=States.PENDING, choices=States.CHOICES)
    output = models.TextField(blank=True)

    class Meta:
        verbose_name = _('Dry run')
        ordering = ('created',)

    class Permissions:
        customer_path = 'order_item_offering__customer'

    @property
    def human_readable_state(self):
        return force_str(dict(self.States.CHOICES)[self.state])

    @transition(field=state, source=States.PENDING, target=States.EXECUTING)
    def set_state_executing(self):
        pass

    @transition(field=state, source=States.EXECUTING, target=States.DONE)
    def set_ok(self):
        pass

    @transition(field=state, source='*', target=States.ERRED)
    def set_erred(self):
        pass
