from django.db.models.signals import pre_save
from django.dispatch import receiver

from core.middleware import get_current_request
from core.models import Vacancy


@receiver(pre_save, sender=Vacancy)
def pre_save_manager(sender, instance, **kwargs):
    request = get_current_request()
    if not instance.manager and not request.user.is_anonymous:
        instance.manager = request.user
