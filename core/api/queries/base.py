import graphene
from django.utils.translation import gettext_lazy as _
from graphene import Int, Argument, String


class GetByIDField(graphene.Field):
    def __init__(self, type_, *args, **kwargs):
        kwargs.setdefault("args", {})
        kwargs["args"].update({
            "id": Argument(Int, required=False, description=_("Django object unique identification field")),
        })
        super().__init__(type_, *args, **kwargs)


class GetBySlugAndIDField(graphene.Field):
    def __init__(self, type_, *args, **kwargs):
        kwargs.setdefault("args", {})
        kwargs["args"].update({
            "id": Argument(Int, required=False, description=_("Django object unique identification field")),
            "slug": Argument(String, required=False, description=_("Django object unique slug field"))
        })
        super().__init__(type_, *args, **kwargs)
