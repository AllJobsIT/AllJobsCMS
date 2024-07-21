import uuid

from dirtyfields import DirtyFieldsMixin
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from modelcluster.models import ClusterableModel
from wagtail import blocks
from wagtail.admin.panels import FieldPanel, InlinePanel, TabbedInterface, ObjectList
from wagtail.blocks import StreamBlock, StructBlock
from wagtail.documents.models import Document
from wagtail.fields import RichTextField, StreamField
from wagtail.search import index
from wagtail.snippets.blocks import SnippetChooserBlock

from core.choices.relationship_type import RelationshipTypeChoice
from core.choices.worker import WorkerProcessStatusChoice
from core.models.snippets.currency import CurrencySnippet
from core.models.snippets.base import Status
from core.panels.worker_panel import SimilarWorkersPanel


# from core.views import generate_docx


class SalaryStructBlock(StructBlock):
    salary_size = blocks.IntegerBlock()
    salary_currency = SnippetChooserBlock(CurrencySnippet)


class SalaryStreamBlock(StreamBlock):
    salary_item = SalaryStructBlock(label=_("Salary item"))


class EnglishGradeStructBlock(StructBlock):
    language = blocks.CharBlock(label=_("Language item"))
    grade = blocks.CharBlock(label=_("Language grade"))


class EnglishGradeStreamBlock(StreamBlock):
    language = EnglishGradeStructBlock(label=_("Language"))


class StackStreamBlock(StreamBlock):
    stack_item = blocks.CharBlock(label=_("Stack item"))


class SkillStreamBlock(StreamBlock):
    skill_item = blocks.CharBlock(label=_("Skill item"))


class ProgrammingLanguageStreamBlock(StreamBlock):
    language_item = blocks.CharBlock(label=_("Programming language"))


class TechnologiesStreamBlock(StreamBlock):
    technology_item = blocks.CharBlock(label=_("Technology item"))


class DatabasesStreamBlock(StreamBlock):
    database_item = blocks.CharBlock(label=_("Database item"))


class SoftwareDevelopmentStreamBlock(StreamBlock):
    software_development_item = blocks.CharBlock(label=_("Software development item"))


class OtherTechnologiesStreamBlock(StreamBlock):
    other_technology_item = blocks.CharBlock(label=_("Other technology item"))


class CertificatesStreamBlock(StreamBlock):
    certificate_item = blocks.CharBlock(label=_("Certificate item"))


class ExampleOfWorkStreamBlock(StreamBlock):
    example_of_work_item = blocks.URLBlock(label=_("Work example item"))


class ContactsStructBlock(StructBlock):
    name = blocks.CharBlock(label=_("Contact type"))
    value = blocks.CharBlock(label=_("Contact value"))


class ContactsStreamBlock(StreamBlock):
    contact = ContactsStructBlock(label=_("Contact item"))


class LinksStructBlock(StructBlock):
    type = blocks.CharBlock(label=_("Link type"))
    link = blocks.URLBlock(label=_("Link value"))


class LinksStreamBlock(StreamBlock):
    link = LinksStructBlock(label=_("Link item"))


class SpecializationStreamBlock(StreamBlock):
    specialization = SnippetChooserBlock("core.Specialization", label=_("Specialization"))


class GradeStreamBlock(StreamBlock):
    grade = SnippetChooserBlock("core.Grade", label=_("Grade"))


class Worker(index.Indexed, DirtyFieldsMixin, ClusterableModel):
    code = models.UUIDField(
        verbose_name=_("Worker unique code"),
        blank=True,
        default=uuid.uuid4,
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("First name"),
        null=True
    )
    last_name = models.CharField(
        max_length=255,
        verbose_name=_("Last name"),
        null=True
    )
    surname = models.CharField(
        max_length=255,
        verbose_name=_("Surname"),
        blank=True,
        null=True
    )
    file = models.ForeignKey(
        Document,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_("File CV")
    )
    telegram_nickname = models.CharField(
        max_length=255,
        verbose_name=_("Telegram nickname"),
        blank=True,
        null=True
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.SET_NULL,
        verbose_name=_("Worker status"),
        blank=True,
        null=True
    )
    status_date = models.DateField(
        verbose_name=_("Changed date status"),
        blank=True,
        null=True,
    )
    type = models.IntegerField(
        choices=RelationshipTypeChoice, default=RelationshipTypeChoice.UNSPECIFIED, verbose_name=_("Relationship type")
    )
    employer = models.CharField(
        max_length=255,
        verbose_name=_("Worker employer"),
        blank=True,
        null=True
    )
    purchase_rate = models.IntegerField(
        verbose_name=_("Purchase rate"),
        blank=True,
        null=True,
    )
    salary = StreamField(
        SalaryStreamBlock(max_num=1), blank=True, null=True, use_json_field=True, verbose_name=_("Worker salary")
    )
    specialization = StreamField(
        SpecializationStreamBlock(), blank=True, null=True, use_json_field=True, verbose_name=_("Worker specialization")
    )
    grade = StreamField(
        GradeStreamBlock(), blank=True, null=True, use_json_field=True, verbose_name=_("Worker grade")
    )
    stack = StreamField(
        StackStreamBlock(), blank=True, null=True, use_json_field=True, verbose_name=_("Worker stacks")
    )
    skills = StreamField(
        SkillStreamBlock(), blank=True, null=True, use_json_field=True, verbose_name=_("Worker skills")
    )
    programming_languages = StreamField(
        ProgrammingLanguageStreamBlock(), blank=True, null=True, use_json_field=True,
        verbose_name=_("Worker programming languages")
    )
    technologies = StreamField(
        TechnologiesStreamBlock(), blank=True, null=True, use_json_field=True,
        verbose_name=_("Worker technologies")
    )
    databases = StreamField(
        DatabasesStreamBlock(), blank=True, null=True, use_json_field=True,
        verbose_name=_("Worker databases")
    )
    software_development = StreamField(
        SoftwareDevelopmentStreamBlock(), blank=True, null=True, use_json_field=True,
        verbose_name=_("Worker software developments")
    )
    other_technologies = StreamField(
        OtherTechnologiesStreamBlock(), blank=True, null=True, use_json_field=True,
        verbose_name=_("Worker other technologies")
    )
    about_worker = RichTextField(
        verbose_name=_("About worker"),
        blank=True,
        null=True
    )
    experience = models.FloatField(
        verbose_name=_("Worker years of experience"),
        blank=True,
        null=True,
        default=0.0
    )
    city = models.CharField(
        max_length=255,
        verbose_name=_("Worker city"),
        blank=True,
        null=True
    )
    citizenship = CountryField(
        verbose_name=_("Worker citizenship"),
        blank=True,
        null=True
    )
    english_grade = StreamField(
        EnglishGradeStreamBlock(), blank=True, null=True, use_json_field=True,
        verbose_name=_("Worker languages")
    )
    education = RichTextField(
        verbose_name=_("Worker education"),
        blank=True,
        null=True
    )
    certificates = StreamField(
        CertificatesStreamBlock(), blank=True, null=True, use_json_field=True,
        verbose_name=_("Worker certificates")
    )
    employer_contact = models.CharField(
        max_length=255,
        verbose_name=_("Worker employer contacts"),
        blank=True,
        null=True
    )
    worker_contact = StreamField(
        ContactsStreamBlock(), blank=True, null=True, use_json_field=True,
        verbose_name=_("Worker contacts")
    )
    example_of_work = StreamField(
        ExampleOfWorkStreamBlock(), blank=True, null=True, use_json_field=True,
        verbose_name=_("Worker example of work")
    )
    links = StreamField(
        LinksStreamBlock(), blank=True, null=True, use_json_field=True,
        verbose_name=_("Worker links")
    )
    comment = RichTextField(
        verbose_name=_("Manager comment about worker"),
        blank=True,
        null=True
    )
    is_published = models.BooleanField(
        default=True,
        verbose_name=_("Is published"),
        blank=True
    )
    birthday = models.DateField(
        verbose_name=_("Worker birthday"),
        blank=True,
        null=True,
    )
    process_status = models.IntegerField(choices=WorkerProcessStatusChoice, default=WorkerProcessStatusChoice.PROCESS,
                                         verbose_name=_("Process status"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    personal_panels = [
        FieldPanel("code", read_only=True),
        FieldPanel("process_status"),
        FieldPanel("last_name"),
        FieldPanel("name"),
        FieldPanel("surname"),
        FieldPanel("birthday"),
        FieldPanel("file"),
        FieldPanel("status"),
        FieldPanel("status_date", read_only=True),
        FieldPanel("type"),
        FieldPanel("employer"),
        FieldPanel("purchase_rate"),
        FieldPanel("salary"),
        FieldPanel("about_worker"),
        FieldPanel("experience"),
        FieldPanel("city"),
        FieldPanel("citizenship"),
        FieldPanel("english_grade"),
        FieldPanel("comment"),
        FieldPanel("is_published"),
    ]

    skills_panels = [
        FieldPanel("specialization"),
        FieldPanel("grade"),
        FieldPanel("stack"),
        FieldPanel("skills"),
        FieldPanel("programming_languages"),
        FieldPanel("technologies"),
        FieldPanel("databases"),
        FieldPanel("software_development"),
        FieldPanel("other_technologies"),
    ]

    work_experience_panels = [
        InlinePanel(
            'work_experiences', label=_("Work Experience")
        ),
    ]

    projects_panels = [
        InlinePanel(
            'projects', label=_("Projects")
        )
    ]

    about_worker_panels = [
        FieldPanel("telegram_nickname"),
        FieldPanel("employer_contact"),
        FieldPanel("worker_contact"),
        FieldPanel("education"),
        FieldPanel("certificates"),
        FieldPanel("example_of_work"),
    ]

    similar_worker_panel = [
        SimilarWorkersPanel(),
    ]

    edit_handler = TabbedInterface([
        ObjectList(personal_panels, heading='Личные данные'),
        ObjectList(about_worker_panels, heading='О кандидате'),
        ObjectList(skills_panels, heading='Навыки и стэк'),
        ObjectList(projects_panels, heading='Проекты работника'),
        ObjectList(work_experience_panels, heading='Опыт работы'),
        ObjectList(similar_worker_panel, heading='Клоны текущей записи'),
    ])

    search_fields = [
        index.SearchField('name'),
        index.SearchField('last_name'),
        index.SearchField('surname'),

        index.AutocompleteField('name'),
        index.AutocompleteField('last_name'),
        index.AutocompleteField('surname'),
    ]

    def __str__(self):
        return f'{self.name} {self.last_name}'

    def full_name(self):
        return f'{self.last_name} {self.name} {self.surname if self.surname else ""}'

    def get_status(self):
        return self.get_process_status_display()

    def get_grade_display(self):
        # Возвращает строковое представление грейда
        return ", ".join([str(item.value) for item in self.grade])

    def get_specialization(self):
        return ", ".join([item.value.title for item in self.specialization])

    def get_type(self):
        return self.get_type_display()

    def get_telegram_nickname(self):
        return mark_safe(
            f"<a href='https://t.me/{self.telegram_nickname}'>{self.telegram_nickname}</a>"
            if self.telegram_nickname and self.telegram_nickname != 'null' else "")

    get_telegram_nickname.admin_order_field = "Telegram"
    get_telegram_nickname.short_description = "Telegram"

    get_grade_display.admin_order_field = "Грейд"
    get_grade_display.short_description = "Грейд"

    full_name.admin_order_field = "Полное имя"
    full_name.short_description = "Полное имя"

    get_status.admin_order_field = "Статус"
    get_status.short_description = "Статус"

    get_type.admin_order_field = "Тип отношений"
    get_type.short_description = "Тип отношений"
