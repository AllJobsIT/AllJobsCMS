import inspect

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from parser_ai.models import Prompt

# @dataclass
# class Prompt:
#     class Method(Enum):
#         REPLACE = "replace"
#         APPEND = "append"
#
#     id: int
#     label: str
#     prompt: str
#     description: str = ""
#     method: Union[str, Method] = Method.REPLACE
#
#     def __post_init__(self):
#         self.prompt = inspect.cleandoc(self.prompt)
#         self.method = Prompt.Method(self.method)
#
#     def as_dict(self) -> dict:
#         return {
#             "id": self.id,
#             "label": self.label,
#             "description": self.description,
#             "prompt": self.prompt,
#             "method": self.method.value,
#         }



def get_prompt_by_id(id: str) -> dict:
    for item in Prompt.objects.all().first().prompts:
        if item.id == id:
            prompt = {
                "id": item.id,
                "label": item.value["label"],
                "description": item.value["description"],
                "prompt": item.value['prompt'],
                "method": item.value['method'],
            }
            return prompt
    return {}
