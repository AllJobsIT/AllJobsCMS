import django_filters
from wagtail.admin.filters import WagtailFilterSet

from core.models.snippets import Worker
from core.models.snippets.base import Grade, Specialization


def get_grades(request):
    return Grade.objects.all()


def get_specializations(request):
    return Specialization.objects.all()


class WorkerFilterSet(WagtailFilterSet):
    grade = django_filters.ModelChoiceFilter(queryset=get_grades, method='filter_by_grade')
    specialization = django_filters.ModelChoiceFilter(queryset=get_specializations, method='filter_by_specialization')

    class Meta:
        model = Worker
        fields = ['grade', 'specialization', 'type', 'process_status', 'input_method']

    def filter_by_grade(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(grade__contains=[{'type': 'grade', 'value': int(value.id)}])

    def filter_by_specialization(self, queryset, name, value):
        if not value:
            return queryset
        return queryset.filter(specialization__contains=[{'type': 'specialization', 'value': int(value.id)}])
