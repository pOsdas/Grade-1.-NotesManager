from datetime import datetime
from dateutil.parser import parse

from utils.declension_of_words import get_word_form


def format_date(date: str) -> datetime:
    try:
        correct_date = parse(date)
        return correct_date
    except ValueError:
        raise ValueError(f"Не удалось обработать ввод даты: {date}")


def give_time(days: int, hours: int, minutes: int) -> str:
    return (
        f"{days} {get_word_form(days, ('день', 'дня', 'дней'))}, "
        f"{hours} {get_word_form(hours, ('час', 'часа', 'часов'))}, "
        f"{minutes} {get_word_form(minutes, ('минута', 'минуты', 'минут'))}."
    )


def compare_dates(issue_date: datetime, status: str) -> str:
    current_time = datetime.now()

    if status == "Отложено":
        return "Отложено"
    if status == "Готово":
        return "Готово"

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
