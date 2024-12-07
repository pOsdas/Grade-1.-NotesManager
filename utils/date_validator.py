from datetime import datetime
from dateutil.parser import parse


def format_date(date: str) -> datetime:
    try:
        correct_date = parse(date)
        return correct_date
    except ValueError:
        raise ValueError(f"Не удалось обработать ввод даты: {date}")


def compare_dates(issue_date: datetime, status: str) -> str:
    current_time = datetime.now()

    if status == "Отложено" or status == "Готово":
        return ""
    if current_time < issue_date:
        remaining_days = issue_date - current_time
        days = remaining_days.days
        hours, remainder = divmod(remaining_days.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        return f"До дедлайна осталось {days} дней, {hours} часов, {minutes} минут."
    elif current_time >= issue_date:
        overdue_days = current_time - issue_date
        days = overdue_days.days
        hours, remainder = divmod(overdue_days.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        return f"Дедлайн просрочен на {days} дней, {hours} часов, {minutes} минут."


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
