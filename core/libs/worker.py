from django.apps import apps



def get_similar_workers(instance):
    Worker = apps.get_model("core", "Worker")
    return Worker.objects.filter(name=instance.name,
                                 birthday=instance.birthday).exclude(pk=instance.pk)


def get_projects_worker(instance):
    Demand = apps.get_model("core", "Demand")
    return Demand.objects.filter(projects__worker=instance).order_by("-projects__date_start")
