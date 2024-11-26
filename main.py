from models.note import Note
from models.user import User


def create_user() -> User:
    username = input("Введите имя пользователя: ")

    created_user = User(username)
    return created_user


def create_note() -> Note:
    title = input("Введите заголовок заметки: ")
    content = input("Введите содержание заметки: ")
    status = input("Введите статус заметки (например, ожидает, готово, в работе): ")
    created_date = input("Введите дату создания заметки (в формате ДД-ММ-ГГГГ): ")
    issue_date = input("Введите дату завершения заметки (в формате ДД-ММ-ГГГГ): ")

    created_note = Note(title, content, status, created_date, issue_date)
    return created_note


if __name__ == "__main__":
    user = create_user()
    print(f"Имя пользователя: {user.username}")

    note = create_note()
    print(f"Заголовок: {note.title}")
    print(f"Статус: {note.status}")
    print(f"Содержание: {note.content}")
    print(f"Дата создания: {note.created_date}")
    print(f"Дата завершения: {note.issue_date}")

