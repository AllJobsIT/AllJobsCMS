import graphene
from django import forms
from django_filters import RangeFilter
from django_filters.utils import get_model_field
from graphene_django.filter import TypedFilter, ListFilter
from graphene_django.filter.utils import get_field_type
from graphene_django.forms import GlobalIDMultipleChoiceField, GlobalIDFormField
from graphene_django.forms.converter import convert_form_field


def get_filtering_args_from_filterset(filterset_class, type, filterset_args=None):
    args = {}
    model = filterset_class._meta.model
    registry = type._meta.registry
    for name, filter_field in filterset_class.base_filters.items():
        filter_type = filter_field.lookup_expr
        required = filter_field.extra.get("required", False)
        field_type = None
        form_field = None

        if (
                isinstance(filter_field, TypedFilter)
                and filter_field.input_type is not None
        ):
            # First check if the filter input type has been explicitly given
            field_type = filter_field.input_type
        else:
            if name not in filterset_class.declared_filters or isinstance(
                    filter_field, TypedFilter
            ):
                # Get the filter field for filters that are no explicitly declared.
                if filter_type == "isnull":
                    field_type = graphene.Boolean
                else:
                    model_field = get_model_field(model, filter_field.field_name)

                    # Get the form field either from:
                    #  1. the formfield corresponding to the model field
                    #  2. the field defined on filter
                    if hasattr(model_field, "formfield"):
                        form_field = model_field.formfield(required=required)
                    if not form_field:
                        form_field = filter_field.field

                    # First try to get the matching field type from the GraphQL DjangoObjectType
                    if model_field:
                        if (
                                isinstance(form_field, forms.ModelChoiceField)
                                or isinstance(form_field, forms.ModelMultipleChoiceField)
                                or isinstance(form_field, GlobalIDMultipleChoiceField)
                                or isinstance(form_field, GlobalIDFormField)
                        ):
                            # Foreign key have dynamic types and filtering on a foreign key actually means filtering on its ID.
                            field_type = get_field_type(
                                registry, model_field.related_model, "id"
                            )
                        else:
                            field_type = get_field_type(
                                registry, model_field.model, model_field.name
                            )

            if not field_type:
                # Fallback on converting the form field either because:
                #  - it's an explicitly declared filters
                #  - we did not manage to get the type from the model type
                form_field = form_field or filter_field.field
                field_type = convert_form_field(form_field).get_type()

            if isinstance(filter_field, ListFilter) or isinstance(
                    filter_field, RangeFilter
            ):
                # Replace InFilter/RangeFilter filters (`in`, `range`) argument type to be a list of
                # the same type as the field. See comments in `replace_csv_filters` method for more details.
                if filterset_args:
                    field_type = graphene.List(filterset_args[name])
                else:
                    field_type = graphene.List(field_type)

        args[name] = graphene.Argument(
            field_type,
            description=filter_field.label,
            required=required,
        )

    return args
