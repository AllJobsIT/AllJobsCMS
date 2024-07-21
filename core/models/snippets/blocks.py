from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.blocks import StructBlock, StreamBlock
from wagtail.snippets.blocks import SnippetChooserBlock


class CostStructBlock(StructBlock):
    size = blocks.IntegerBlock(label=_("Cost size"))
    currency = SnippetChooserBlock("core.CurrencySnippet", label=_("Cost currency"))


class CostStreamBlock(StreamBlock):
    cost_item = CostStructBlock(label=_("Cost item"))
