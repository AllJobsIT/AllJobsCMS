from django.db import models
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel


class CurrencySnippet(models.Model):
    char_code = models.CharField(_('Currency code'), max_length=3, unique=True)
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    symbol = models.CharField(verbose_name=_('Currency symbol'), max_length=4)

    panels = [
        FieldPanel("char_code"),
        FieldPanel("name"),
        FieldPanel("symbol")
    ]

    class Meta:
        verbose_name = _("Currency")
        verbose_name_plural = _("Currencies")

    def __str__(self):
        return f"{self.name} - {self.symbol}"
