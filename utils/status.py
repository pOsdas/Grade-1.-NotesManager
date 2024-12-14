def check_status(status: str) -> bool:
    allowed_statuses = {"В ожидании", "Готово", "Отложено", "Просрочено"}
    if status not in allowed_statuses:
        raise ValueError(f"Недопустимый статус: {status}. Возможные значения: {', '.join(allowed_statuses)}")
    return True


