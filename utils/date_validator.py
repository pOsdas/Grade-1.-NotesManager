from datetime import datetime
from dateutil.parser import parse


def format_date(date: str) -> datetime:
    try:
        correct_date = parse(date)
        return correct_date
    except ValueError:
        raise ValueError(f"Не удалось обработать ввод даты: {date}")


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
