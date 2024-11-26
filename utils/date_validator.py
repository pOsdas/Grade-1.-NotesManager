from datetime import datetime

# created_date = "11-25-2024"
# issue_date = "26-Nov-2024"


def format_date(date: str) -> str:
    formats = [
        "%d-%m-%Y",  # 25-11-2024
        "%d.%m.%y",  # 25.11.24
        "%d:%m:%y",  # 25:11:24
        "%m-%d-%Y",  # 11-25-24
        "%d-%b-%Y",  # 25-Nov-2024
    ]
    for form in formats:
        try:
            correct_date = datetime.strptime(date, form)
            return correct_date.strftime("%d-%m")
        except ValueError:
            continue
    return "Некорректный формат даты"


# temp_created_date = format_date(created_date)
# temp_issue_date = format_date(issue_date)
#
# print(f"Дата создания: {temp_created_date}")
# print(f"Дата задачи: {temp_issue_date}")