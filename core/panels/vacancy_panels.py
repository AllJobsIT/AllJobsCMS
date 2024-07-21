from wagtail.admin.panels import Panel

from core.libs.worker import get_eligible_workers


class EligibleWorkersPanel(Panel):
    class BoundPanel(Panel.BoundPanel):
        template_name = "eligible_workers_pamel.html"
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
            eligible_workers = get_eligible_workers(instance)

            context.update({
                'instance': instance,
                'eligible_workers': eligible_workers,
            })
            return context
