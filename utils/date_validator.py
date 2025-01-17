from datetime import datetime
import re

from utils.declension_of_words import get_word_form
from utils.status import display_note_status


def format_date(date_str: str) -> datetime:
    formats = [
        (r"^\d{4}-\d{2}-\d{2}$", "%Y-%m-%d"),  # 2024-12-14
        (r"^\d{4}:\d{2}:\d{2}$", "%Y:%m:%d"),  # 2024:12:14
        (r"^\d{4}/\d{2}/\d{2}$", "%Y/%m/%d"),  # 2024/12/14
        (r"^\d{4}\.\d{2}\.\d{2}$", "%Y.%m.%d"),  # 2024.12.14
        (r"^\d{2}-\d{2}-\d{4}$", "%d-%m-%Y"),  # 14-12-2024
        (r"^\d{2}/\d{2}/\d{4}$", "%d/%m/%Y"),  # 14/12/2024
        (r"^\d{2}\.\d{2}\.\d{4}$", "%d.%m.%Y"),  # 14.12.2024
        (r"^\d{2}\:\d{2}\:\d{4}$", "%d:%m:%Y"),  # 14:12:2024
    ]

    for pattern, date_format in formats:
        if re.match(pattern, date_str):
            try:
                parsed_date = datetime.strptime(date_str, date_format)
                return parsed_date
            except ValueError:
                raise ValueError(f"Некорректный формат даты: {date_str}")

    raise ValueError(f"Формат даты не поддерживается: {date_str}")


def give_time(days: int, hours: int, minutes: int) -> str:
    return (
        f"{days} {get_word_form(days, ('день', 'дня', 'дней'))}, "
        f"{hours} {get_word_form(hours, ('час', 'часа', 'часов'))}, "
        f"{minutes} {get_word_form(minutes, ('минута', 'минуты', 'минут'))}."
    )


def compare_dates(issue_date: datetime, status: str) -> str:
    current_time = datetime.now()

    if status == "Отложено":
        return f"{display_note_status('Отложено')}"
    if status == "Готово":
        return f"{display_note_status('Готово')}"

    if current_time < issue_date:
        remaining_days = issue_date - current_time
        days = remaining_days.days
        hours, remainder = divmod(remaining_days.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        return f"До дедлайна осталось {give_time(days, hours, minutes)}"

    elif current_time >= issue_date:
        overdue_days = current_time - issue_date
        days = overdue_days.days
        hours, remainder = divmod(overdue_days.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        return f"Дедлайн просрочен на {give_time(days, hours, minutes)}"


# transfer from str to datetime object
# def handle_date(value):
#     if isinstance(value, str) and value:
#         try:
#             return datetime.strptime(value, '%Y-%m-%d')
#         except ValueError:
#             raise ValueError(f"Некорректный формат даты: {value}")
#     elif value is None or value == "":
#         return None
#
#     return value
