import re


def clean_string(string_value):
    # Удалить все символы, кроме цифр, точек и запятых
    cleaned_string = re.sub(r'[^0-9.,]', '', string_value)
    # Заменить запятые на точки, если нужно
    cleaned_string = cleaned_string.replace(',', '.')
    return cleaned_string


def string_to_integer(string_value):
    try:
        # Очистить строку от лишних символов
        cleaned_string = clean_string(string_value)
        int_value = int(cleaned_string)
        return int_value
    except (ValueError, ArithmeticError, TypeError) as e:
        # Обработка ошибки преобразования
        print(f"Ошибка преобразования строки в Integer: {e}")
        return None


def format_years(number):
    if number % 10 == 1 and number % 100 != 11:
        return f"{number} год"
    elif 2 <= number % 10 <= 4 and not (10 <= number % 100 <= 20):
        return f"{number} года"
    else:
        return f"{number} лет"
