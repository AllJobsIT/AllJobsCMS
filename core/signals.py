from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

from core.models.snippets import Worker


@receiver(pre_save, sender=Worker)
def update_status_date(sender, instance, **kwargs):
    dirty_fields = instance.get_dirty_fields(check_relationship=True)
    if 'status' in dirty_fields:
        instance.status_date = timezone.now()
