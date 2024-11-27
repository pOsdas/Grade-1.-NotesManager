from models.note import Note
from models.user import User


def create_user() -> User:
    username = input("Введите имя пользователя: ")

    return User(username)


def create_note() -> Note:
    title = input("Введите заголовок заметки: ")
    content = input("Введите содержание заметки: ")
    status = input("Введите статус заметки (например, ожидает, готово, в работе): ")
    created_date = input("Введите дату создания заметки (в формате ДД-ММ-ГГГГ): ")
    issue_date = input("Введите дату завершения заметки (в формате ДД-ММ-ГГГГ): ")

    return Note(
        username=user.username,
        title=title,
        content=content,
        status=status,
        created_date=created_date,
        issue_date=issue_date,
    )


if __name__ == "__main__":
    user = create_user()
    print(f"Пользователь создан: {user}")

    note = create_note()
    print(f"Заметка создана:\n{note}")

