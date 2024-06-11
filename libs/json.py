import json


def json_to_dict(json_message):
    try:
        # Удаляем ключевое слово ```json``` и любые окружающие пробелы или новые строки
        clean_message = json_message.strip().lstrip('```json').rstrip('```').strip()
        # Конвертация очищенного JSON-сообщения в словарь
        dictionary = json.loads(clean_message)
        return dictionary
    except json.JSONDecodeError as e:
        # Обработка ошибки декодирования JSON
        print(f"Ошибка декодирования JSON: {e}")
        return None
