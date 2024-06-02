from wagtail.snippets.models import register_snippet
from wagtail.snippets.views.snippets import SnippetViewSet

from core.models.snippets import Worker, Status, Type, Specialization, Grade, EnglishGrade, Project, Rank
from core.models.snippets.candidate import Candidate
from core.models.snippets.demand import Demand, DemandTimeLog
from core.models.snippets.steps_in_board import StepsInBoard


@register_snippet
class WorkersSnippetViewSet(SnippetViewSet):
    model = Worker
    menu_label = 'Worker'
    menu_icon = 'user'
    menu_order = 200
    add_to_settings_menu = False
    add_to_admin_menu = True
    list_display = ('full_name', )


@register_snippet
class ProjectSnippetViewSet(SnippetViewSet):
    model = Project
    menu_label = 'Project'
    menu_icon = 'user'
    menu_order = 200
    add_to_settings_menu = False
    list_display = ('title', 'worker')


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
class CandidateSnippetViewSet(SnippetViewSet):
    model = Candidate
    menu_label = 'Candidate'
    menu_icon = 'user'
    menu_order = 200
    add_to_settings_menu = False
    add_to_admin_menu = True
    exclude_from_explorer = False
    list_display = ('telegram_nickname',)


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
class DemandSnippetViewSet(SnippetViewSet):
    model = Demand
    menu_label = 'Demand'
    menu_icon = 'user'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('display_name',)


@register_snippet
class DemandTimeLogSnippetViewSet(SnippetViewSet):
    model = DemandTimeLog
    menu_label = 'Demand Time Log'
    menu_icon = 'user'
    menu_order = 200
    add_to_settings_menu = True
    exclude_from_explorer = False
    list_display = ('demand__display_name',)

