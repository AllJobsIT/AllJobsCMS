from django.template.loader import render_to_string
from django.utils.html import format_html
from wagtail.admin.panels import Panel

from core.libs.worker import get_similar_workers


class SimilarWorkersPanel(Panel):
    class BoundPanel(Panel.BoundPanel):
        template_name = "similar_worker_panel.html"
        # Default icons for common model field types,
        # based on the corresponding FieldBlock's icon.
        default_field_icons = {
            "DateField": "date",
            "TimeField": "time",
            "DateTimeField": "date",
            "URLField": "link-external",
            "TaggableManager": "tag",
            "EmailField": "mail",
            "TextField": "pilcrow",
            "RichTextField": "pilcrow",
            "FloatField": "decimal",
            "DecimalField": "decimal",
            "BooleanField": "tick-inverse",
        }

        def get_context_data(self, parent_context=None):
            context = super().get_context_data(parent_context)
            instance = context['self'].instance
            similar_workers = get_similar_workers(instance)

            context.update({
                'instance': instance,
                'similar_workers': similar_workers,
            })
            return context

    def clone(self):
        return self.__class__()

    def render_html(self, parent_context):
        instance = parent_context['instance']
        similar_workers = instance.similar_workers.all()

        context = {
            'instance': instance,
            'similar_workers': similar_workers,
        }

        return format_html(render_to_string('similar_worker_panel.html', context))
