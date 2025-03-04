from graphene import String, List, ObjectType, Field
from graphene.types.generic import GenericScalar
from graphene_django import DjangoObjectType

from core.models import Worker

class WorkerType(DjangoObjectType):
    class Meta:
        model = Worker
        fields = (
            'id', 'code', 'name', 'last_name', 'surname', 'telegram_nickname', 'type', 'employer', 'purchase_rate',
            'about_worker', 'experience', 'city', 'citizenship', 'education', 'employer_contact', 'comment',
            'ai_comment', 'is_published', 'birthday', "updated_at", "created_at"
        )

    english_grade = Field(GenericScalar)
    worker_contact = Field(GenericScalar)
    links = Field(GenericScalar)
    salary = String()
    stack = List(String)
    skills = List(String)
    programming_languages = List(String)
    technologies = List(String)
    databases = List(String)
    software_development = List(String)
    other_technologies = List(String)
    certificates = List(String)
    example_of_work = List(String)
    full_name = String()
    status = String()
    grade = String()
    specialization = String()
    type = String()
    telegram_nickname = String()
    ai_comment = Field(GenericScalar)

    def resolve_ai_comment(self, info):
        if self.ai_comment:
            return self.ai_comment_json

    # TODO: эти 3 метода скорее придется изменить на список, смотря как удобно будет фронту
    def resolve_english_grade(self, info):
        if self.english_grade:
            return {item.value["language"]: item.value["grade"] for item in self.english_grade}
        return {}

    def resolve_worker_contact(self, info):
        if self.worker_contact:
            return {item.value["name"]: item.value["value"] for item in self.worker_contact}
        return {}

    def resolve_links(self, info):
        if self.links:
            return {item.value["name"]: item.value["value"] for item in self.links}
        return {}

    def resolve_stack(self, info):
        return [item.value for item in self.stack] if self.stack else []

    def resolve_skills(self, info):
        return [item.value for item in self.skills] if self.skills else []

    def resolve_programming_languages(self, info):
        return [item.value for item in self.programming_languages] if self.programming_languages else []

    def resolve_technologies(self, info):
        return [item.value for item in self.technologies] if self.technologies else []

    def resolve_databases(self, info):
        return [item.value for item in self.databases] if self.databases else []

    def resolve_software_development(self, info):
        return [item.value for item in self.software_development] if self.software_development else []

    def resolve_other_technologies(self, info):
        return [item.value for item in self.other_technologies] if self.other_technologies else []

    def resolve_certificates(self, info):
        return [item.value for item in self.certificates] if self.certificates else []

    def resolve_example_of_work(self, info):
        return [item.value for item in self.example_of_work] if self.example_of_work else []

    def resolve_salary(self, info):
        return self.get_salary()

    def resolve_full_name(self, info):
        return self.full_name()

    def resolve_status(self, info):
        return self.get_status()

    def resolve_grade(self, info):
        return self.get_grade_display()

    def resolve_specialization(self, info):
        return self.get_specialization()

    def resolve_type(self, info):
        return self.get_type()

    def resolve_telegram_nickname(self, info):
        return self.get_telegram_nickname()
