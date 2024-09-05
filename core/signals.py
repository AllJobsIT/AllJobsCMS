from django.db.models.signals import pre_save
from django.dispatch import receiver

from core.middleware import get_current_request
from core.models.snippets.demand import Demand


@receiver(pre_save, sender=Demand)
def pre_save_demands(sender, instance, **kwargs):
    request = get_current_request()
    if not instance.manager:
        instance.manager = request.user
