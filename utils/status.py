from colorama import Fore, Style


def check_status(status: str) -> bool:
    allowed_statuses = {"В ожидании", "Готово", "Отложено", "Просрочено"}
    if status not in allowed_statuses:
        raise ValueError(f"Недопустимый статус: {status}. Возможные значения: {', '.join(allowed_statuses)} ⚠️")
    return True


STATUS_COLORS = {
    "В ожидании": Fore.YELLOW,
    "Готово": Fore.GREEN,
    "Отложено": Fore.BLUE,
    "Просрочено": Fore.RED,
}


def display_note_status(status: str) -> str:
    color = STATUS_COLORS.get(status, Fore.WHITE)
    return f"{color}{status}{Style.RESET_ALL}"


