from django.apps import apps


def get_similar_workers(instance):
    Worker = apps.get_model("core", "Worker")
    return Worker.objects.filter(name=instance.name,
                                 birthday=instance.birthday).exclude(pk=instance.pk)
