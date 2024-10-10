import inspect

from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from parser_ai.models import Prompt


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
