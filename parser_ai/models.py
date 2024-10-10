import inspect

from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.blocks import StreamBlock, StructBlock
from wagtail.contrib.settings.models import BaseGenericSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.fields import StreamField

from parser_ai.choices.prompts import MethodChoice


class PromptStructBlock(StructBlock):
    label = blocks.CharBlock(max_length=64, verbose_name=_("Prompt label"))
    prompt = blocks.TextBlock(max_length=1024, verbose_name=_("Prompt"))
    description = blocks.TextBlock(max_length=1024, verbose_name=_("Prompt description"))
    method = blocks.ChoiceBlock(choices=MethodChoice.choices, default=MethodChoice.REPLACE)


class PromptStreamBlock(StreamBlock):
    prompt = PromptStructBlock()


@register_setting
class Prompt(BaseGenericSetting):
    prompts = StreamField(
        PromptStreamBlock(), blank=True, null=True, use_json_field=True, verbose_name=_("Prompts")
    )

    def as_dict(self) -> list:
        prompts = [{
            "id": item.id,
            "label": item.value["label"],
            "description": item.value["description"],
            "prompt": item.value['prompt'],
            "method": item.value['method'],
        } for item in self.prompts]
        return prompts

    class Meta:
        verbose_name = _("Prompt")
        verbose_name_plural = _("Prompts")
