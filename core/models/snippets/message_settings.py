from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.settings.models import BaseGenericSetting
from wagtail.contrib.settings.registry import register_setting
from wagtailmarkdown.fields import MarkdownField


@register_setting
class MessageSettings(BaseGenericSetting):
    text = MarkdownField(
        default="""{{ tags }}

**{{ title }}**
{% for grade in grades %} {{ grade }} {% endfor %}

**Требования к кандидату:**
{% for item in requirements %}
{{ item }}
{% endfor %}

**Обязанности кандидата:**
{% for item in responsibilities %}
{{ item }}
{% endfor %}""",
        help_text=mark_safe(
            "Эта настройка отвечает за то, как будет выглядеть сообщение в канале телеграмма для всех вакансий. "
            "Это шаблон!<br/>"
            "Здесь работает шаблонизатор jinja2.<br/>"
            "Для того, чтобы сделать цикл по элементам:<br/>"
            "{% for item in [название переменной] %}<br/>"
            "{{ item }}<br/>"
            "{% endfor %}<br/>"
            "Для того, чтобы сделать условие:<br/>"
            "{% if [название переменной] %}<br/>"
            "[какие либо действия, будь то вывод переменной или цикл]<br/>"
            "{% endif %}<br/>"
            "{{ title }} - Заголовок вакансии<br/>"
            "{{ specialization }} - Специализация вакансии<br/>"
            "{{ stack }} - Стэк вакансии<br/>"
            "{{ requirements }} - Требования к кандидату<br/>"
            "{{ responsibilities }} - Обязанности кандидата<br/>"
            "{{ cost }} - Рейт вакансии<br>"
            "{{ location }} - Локация<br>"
            "{{ load }} - Загруженность<br>"
            "{{ tags }} - Тэги. Будут выводиться в формате тг, то есть с #<br>"
            "{{ grades }} - Грейд вакансии"
        )
    )

    panels = [
        FieldPanel('text'),
    ]

    class Meta:
        verbose_name = _("Message template")
