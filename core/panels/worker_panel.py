from django.template.loader import render_to_string
from django.utils.html import format_html
from wagtail.admin.panels import Panel

from core.libs.worker import get_similar_workers, get_projects_worker


class ProjectsWorkersPanel(Panel):
    class BoundPanel(Panel.BoundPanel):
        template_name = "worker_projects_panel.html"
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
            projects = get_projects_worker(instance)

            context.update({
                'instance': instance,
                'projects': projects,
            })
            return context


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
