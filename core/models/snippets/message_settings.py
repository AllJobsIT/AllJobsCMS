from django.utils.safestring import mark_safe
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField

from core.models.snippets.base import BaseSnippet


class MessageSettings(BaseSnippet):
    text = RichTextField(max_length=2056,
                         help_text=mark_safe(
                             "Эта настройка отвечает за то, как будет выглядеть сообщение в канале телеграмма для "
                             "всех вакансий. Это шаблон!\<br/>"
                             "$title - Заголовок вакансии<br/>"
                             "$requirements - Требования к кандидату<br/>"
                             "$responsibilities - Обязанности кандидата<br/>"
                             "$cost - Рейт вакансии<br>"
                             "$location - Локация<br>"
                             "$load - Загруженность<br>"
                             "$tags - Тэги. Будут выводиться в формате тг, то есть с #<br>"
                             "$grade - Грейд вакансии")
                         )

    panels = [
        FieldPanel('text'),
    ]
