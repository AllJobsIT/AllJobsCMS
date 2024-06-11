from django.templatetags.static import static
from django.utils.html import format_html
from wagtail import hooks
from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from core.models.snippets import Worker, Status, Type, Specialization, Grade, EnglishGrade, Rank
from core.models.snippets.steps_in_board import StepsInBoard
from core.models.snippets.vacancy import Vacancy


@register_snippet
class WorkersSnippetViewSet(SnippetViewSet):
    model = Worker
    menu_label = 'Worker'
    menu_icon = 'user'
    menu_order = 200
    add_to_settings_menu = False
    add_to_admin_menu = True
    list_display = ('full_name',)


@register_snippet
class StatusSnippetViewSet(SnippetViewSet):
    model = Status
    menu_label = 'Status'
    menu_icon = 'user'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('title',)


@register_snippet
class TypeSnippetViewSet(SnippetViewSet):
    model = Type
    menu_label = 'Type'
    menu_icon = 'user'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('title',)


@register_snippet
class TypeSnippetViewSet(SnippetViewSet):
    model = Rank
    menu_label = 'Rank'
    menu_icon = 'user'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('name',)


@register_snippet
class SpecializationSnippetViewSet(SnippetViewSet):
    model = Specialization
    menu_label = 'Specialization'
    menu_icon = 'user'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('title',)


@register_snippet
class GradeSnippetViewSet(SnippetViewSet):
    model = Grade
    menu_label = 'Grade'
    menu_icon = 'user'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('title',)


@register_snippet
class EnglishGradeSnippetViewSet(SnippetViewSet):
    model = EnglishGrade
    menu_label = 'English Grade'
    menu_icon = 'user'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('title',)


@register_snippet
class StepsInBoardSnippetViewSet(SnippetViewSet):
    model = StepsInBoard
    menu_label = 'Steps In Board'
    menu_icon = 'user'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('name',)


@register_snippet
class VacancySnippetViewSet(SnippetViewSet):
    model = Vacancy
    menu_label = 'Vacancies'
    menu_icon = 'user'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('title', 'get_status_display')
