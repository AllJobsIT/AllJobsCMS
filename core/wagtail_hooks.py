from django.templatetags.static import static
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from wagtail import hooks
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet
from wagtail.snippets.widgets import SnippetListingButton

from core.libs.filters import WorkerFilterSet, VacancyFilterSet
from core.models.snippets import Worker, Status, Type, Rank
from core.models.snippets.base import Specialization, Grade
from core.models.snippets.steps_in_board import StepsInBoard
from core.models.snippets.vacancy import Vacancy


@register_snippet
class WorkersSnippetViewSet(SnippetViewSet):
    model = Worker
    menu_label = _('Workers')
    menu_icon = 'user'
    menu_order = 200
    add_to_settings_menu = False
    add_to_admin_menu = True
    filterset_class = WorkerFilterSet
    list_display = (
        'full_name', 'employer', 'purchase_rate', 'specialization', 'get_grade_display', 'experience', 'city',
        'get_telegram_nickname', "get_status")


@register_snippet
class VacancySnippetViewSet(SnippetViewSet):
    model = Vacancy
    menu_label = _('Vacancies')
    menu_icon = 'doc-full'
    menu_order = 200
    add_to_settings_menu = False
    add_to_admin_menu = True
    exclude_from_explorer = False
    filterset_class = VacancyFilterSet
    list_display = (
        'title', 'created_at', 'specialization', 'grades', 'cost', 'get_status', 'get_stack_display', "uuid")


@register_snippet
class StatusSnippetViewSet(SnippetViewSet):
    model = Status
    menu_label = _('Status')
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('title',)


@register_snippet
class TypeSnippetViewSet(SnippetViewSet):
    model = Type
    menu_label = _('Type')
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('title',)


@register_snippet
class RankSnippetViewSet(SnippetViewSet):
    model = Rank
    menu_label = _('Rank')
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('name',)


@register_snippet
class SpecializationSnippetViewSet(SnippetViewSet):
    model = Specialization
    menu_label = _('Specialization')
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('title',)


@register_snippet
class GradeSnippetViewSet(SnippetViewSet):
    model = Grade
    menu_label = _('Grade')
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('title',)


@register_snippet
class StepsInBoardSnippetViewSet(SnippetViewSet):
    model = StepsInBoard
    menu_label = _('Steps In Board')
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('name',)


@hooks.register('insert_global_admin_css')
def global_admin_css():
    return format_html('<link rel="stylesheet" href="{}">', static('css/index.css'))


@hooks.register('register_snippet_listing_buttons')
def register_snippet_listing_buttons(snippet, user, next):
    if isinstance(snippet, Worker):
        docx_url = reverse('download_docx', args=[snippet.id])
        pdf_url = reverse('download_pdf', args=[snippet.id])
        view_url = reverse('view_template', args=[snippet.id])
        return [
            SnippetListingButton(
                _('Download DOCX'),
                docx_url,
                priority=50,
                icon_name="doc-full"
            ),
            SnippetListingButton(
                _('Download PDF'),
                pdf_url,
                priority=60,
                icon_name="form"
            ),
            SnippetListingButton(
                _('Check template'),
                view_url,
                priority=70,
                icon_name="draft",
            ),
        ]
    return []
