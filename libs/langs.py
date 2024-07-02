from babel import Locale
from django.utils.translation import gettext_lazy as _


def get_language_name(char_code):
    locale = Locale.parse(char_code.lower())
    return _(locale.get_display_name(locale='en'))
