import json
import re


def is_valid_json(text):
    try:
        json.loads(text)
        return True
    except json.JSONDecodeError:
        return False


def json_to_dict(json_message):
    pattern = re.compile(r'```json(.*?)```', re.DOTALL)
    matches = pattern.findall(json_message)
    json_objects = [
        json.loads(match.strip())
        for match in matches
        if is_valid_json(match.strip())
    ]

    return json_objects[0]
