from django.apps import apps
from django.db.models import Q


def get_similar_workers(instance):
    Worker = apps.get_model("core", "Worker")
    return Worker.objects.filter(name=instance.name,
                                 birthday=instance.birthday).exclude(pk=instance.pk)


def get_projects_worker(instance):
    Demand = apps.get_model("core", "Demand")
    return Demand.objects.filter(projects__worker=instance)


def get_eligible_workers(instance):
    Worker = apps.get_model("core", "Worker")

    specialization_ids = [
        item.value.id for item in instance.specialization
    ]
    stacks = [
        item.value for item in instance.stack
    ]
    filters = Q()
    if specialization_ids:
        spec_filters = Q()
        for spec_id in specialization_ids:
            spec_filters |= Q(specialization__contains=[{"value": spec_id}])
        filters &= spec_filters
    if stacks:
        stack_filters = Q()
        for stack in stacks:
            stack_filters |= Q(stack__contains=[{"value": stack}])
        filters &= stack_filters
    filters &= Q(purchase_rate__lt=instance.cost or 999999)
    workers = Worker.objects.filter(filters).distinct()
    print(workers.query)
    return workers
