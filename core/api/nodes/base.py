from collections import OrderedDict
from functools import partial

from django.db.models import QuerySet
from graphene import Field, ObjectType, Int, String
from graphene_django import DjangoObjectType, DjangoListField
from graphene_django.filter.utils import get_filterset_class
from graphene_django.registry import get_global_registry
from graphene_django.utils import is_valid_django_model, DJANGO_FILTER_INSTALLED, maybe_queryset
from graphene_django_extras import DjangoObjectField
from graphene_django_extras.base_types import factory_type, DjangoListObjectBase
from graphene_django_extras.paginations.pagination import BaseDjangoGraphqlPagination
from graphene_django_extras.settings import graphql_api_settings
from graphene_django_extras.types import DjangoObjectOptions
from graphene_django_extras.utils import queryset_factory

from core.api.libs.utils import get_filtering_args_from_filterset


class CustomDjangoListObjectType(ObjectType):
    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(
            cls,
            model=None,
            registry=None,
            results_field_name=None,
            pagination=None,
            only_fields=(),
            exclude_fields=(),
            filter_fields=None,
            queryset=None,
            filterset_class=None,
            base_type=None,
            **options,
    ):

        assert is_valid_django_model(model), (
            'You need to pass a valid Django Model in {}.Meta, received "{}".'
        ).format(cls.__name__, model)

        if not registry:
            registry = get_global_registry()

        if not DJANGO_FILTER_INSTALLED and filter_fields:
            raise Exception("Can only set filter_fields if Django-Filter is installed")

        assert isinstance(queryset, QuerySet) or queryset is None, (
            "The attribute queryset in {} needs to be an instance of "
            'Django model queryset, received "{}".'
        ).format(cls.__name__, queryset)

        results_field_name = results_field_name or "results"

        baseType = base_type

        if not baseType:
            factory_kwargs = {
                "model": model,
                "only_fields": only_fields,
                "exclude_fields": exclude_fields,
                "filter_fields": filter_fields,
                "filterset_class": filterset_class,
                "pagination": pagination,
                "queryset": queryset,
                "registry": registry,
                "skip_registry": False,
            }
            baseType = factory_type("output", DjangoObjectType, **factory_kwargs)

        filter_fields = filter_fields or baseType._meta.filter_fields

        if pagination:
            result_container = pagination.get_pagination_field(baseType)
        else:
            global_paginator = graphql_api_settings.DEFAULT_PAGINATION_CLASS
            if global_paginator:
                assert issubclass(global_paginator, BaseDjangoGraphqlPagination), (
                    'You need to pass a valid DjangoGraphqlPagination class in {}.Meta, received "{}".'
                ).format(cls.__name__, global_paginator)

                global_paginator = global_paginator()
                result_container = global_paginator.get_pagination_field(baseType)
            else:
                result_container = DjangoListField(baseType)

        _meta = DjangoObjectOptions(cls)
        _meta.model = model
        _meta.registry = registry
        _meta.queryset = queryset
        _meta.baseType = baseType
        _meta.results_field_name = results_field_name
        _meta.filter_fields = filter_fields
        _meta.exclude_fields = exclude_fields
        _meta.only_fields = only_fields
        _meta.filterset_class = filterset_class
        _meta.fields = OrderedDict(
            [
                (results_field_name, result_container),
                (
                    "count",
                    Field(
                        Int,
                        name="totalCount",
                        description="Total count of matches elements",
                    ),
                ),
            ]
        )

        super(CustomDjangoListObjectType, cls).__init_subclass_with_meta__(
            _meta=_meta, **options
        )

    @classmethod
    def RetrieveField(cls, *args, **kwargs):
        return DjangoObjectField(cls._meta.baseType, **kwargs)

    @classmethod
    def BaseType(cls):
        return cls._meta.baseType


class CustomDjangoListObjectField(Field):
    def __init__(
            self,
            _type,
            fields=None,
            extra_filter_meta=None,
            filterset_class=None,
            filterset_args_classes=None,
            *args,
            **kwargs,
    ):
        self.parent = _type
        if DJANGO_FILTER_INSTALLED:
            _fields = _type._meta.filter_fields
            _model = _type._meta.model

            self.fields = fields or _fields

            meta = dict(model=_model, fields=self.fields)
            if extra_filter_meta:
                meta.update(extra_filter_meta)

            filterset_class = filterset_class or _type._meta.filterset_class
            self.filterset_class = get_filterset_class(filterset_class, **meta)
            self.filtering_args = get_filtering_args_from_filterset(
                self.filterset_class, _type, filterset_args_classes
            )
            kwargs.setdefault("args", {})
            kwargs["args"].update(self.filtering_args)

        if not kwargs.get("description", None):
            kwargs["description"] = "{} list".format(_type._meta.model.__name__)

        super(CustomDjangoListObjectField, self).__init__(_type, *args, **kwargs)

    @property
    def model(self):
        return self.type._meta.model

    def list_resolver(
            self, manager, filterset_class, filtering_args, root, info, **kwargs
    ):

        qs = queryset_factory(manager, root, info, **kwargs)

        filter_kwargs = {k: v for k, v in kwargs.items() if k in filtering_args}

        qs = filterset_class(data=filter_kwargs, queryset=qs, request=info.context).qs
        count = qs.count()

        return DjangoListObjectBase(
            count=count,
            results=maybe_queryset(qs),
            results_field_name=self.type._meta.results_field_name
        )

    def wrap_resolve(self, parent_resolver):
        return partial(
            self.list_resolver,
            self.type._meta.model._default_manager,
            self.filterset_class,
            self.filtering_args,
        )


class KeyValueType(ObjectType):
    key = String()
    value = String()
