from django.db import models
from wagtail.blocks import StreamBlock, StructBlock
from wagtail.contrib.settings.models import BaseGenericSetting
from wagtail.contrib.settings.registry import register_setting
from wagtail.fields import StreamField
from django.utils.translation import gettext_lazy as _

from core.models.snippets import blocks


class ChatStructBlock(StructBlock):
    chat_name = blocks.CharBlock(max_length=256, label=_("Chat name"))
    chat_id = blocks.CharBlock(max_length=128, label=_("Chat id"))


class ChatsStreamBlock(StreamBlock):
    chat = ChatStructBlock(label=_("Chat"))


@register_setting
class ChatIds(BaseGenericSetting):
    message = models.TextField(max_length=2048, default='')
    chats = StreamField(
        ChatsStreamBlock(), blank=True, null=True, use_json_field=True, verbose_name=_("Chats")
    )

    class Meta:
        verbose_name = _("Chat for mailing")
        verbose_name_plural = _("Chats for mailing")

