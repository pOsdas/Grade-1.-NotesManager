from sqlalchemy.exc import IntegrityError

from utils.date_validator import format_date
from database.db import init_db, SessionLocal
from models.note import Note
from models.user import User


def create_user(
        current_session,
        username: str,
) -> None | User:
    new_user = User(username=username)
    try:
        current_session.add(new_user)
        current_session.commit()
        print(f"Пользователь '{username}' создан успешно!")
    except IntegrityError:
        current_session.rollback()
        print(f"Пользователь '{username}' уже существует.")
    return new_user


def create_note(
        current_session,
        username: str,
        title: str,
        content: str,
        status: str,
        issue_date: str,
) -> Note | None:

    current_user = current_session.query(User).filter(User.username == username).first()
    if not current_user:
        print(f"Пользователь '{username}' не найден.")
        return None

    current_note = Note(
        title=title,
        content=content,
        status=status,
        issue_date=format_date(issue_date),
        user_id=current_user.id,
    )
    session.add(current_note)
    session.commit()
    print(f"Заметка '{title}' добавлена для пользователя '{username}'.")
    return current_note


def get_note(current_session, username: str) -> list:
    try:
        current_user = current_session.query(User).filter_by(username=username).first()
        if not current_user:
            print(f"Пользователь с именем {username} не найден.")
            return []
        notes = current_session.query(Note).filter_by(user_id=current_user.id).all()
        if not notes:
            print(f"У пользователя {username} нет заметок.")
            return []

        print(f"Заметки пользователя {username}:")
        print("-" * 40)
        # Выводим каждую заметку
        for one_note in notes:
            print(f"Заголовок: {one_note.title}")
            print(f"Содержание: {one_note.content}")
            print(f"Статус: {one_note.status}")
            print(f"Дата создания: {one_note.created_date}")
            print(f"Дата завершения: {one_note.issue_date}")
            print("-" * 40)

        return notes

    except Exception as e:
        print(f"Ошибка при получении заметок: {e}")
        return []

    finally:
        session.close()


def current_user_info(current_session, username: str, note_name: str) -> Note | None:
    current_user = current_session.query(User).filter_by(username=username).first()

    if not current_user:
        print(f"Пользователь с именем {username} не найден.")
        return

    note_info = current_session.query(Note).filter_by(title=note_name, user_id=current_user.id).first()
    return note_info


def update_note_status(current_session, username: str, note_name: str, new_status: str) -> None:
    try:
        current_note = current_user_info(current_session, username, note_name)

        if not current_note:
            print(f"Заметка с названием {note_name} не найдена у пользователя {username}.")
            return

        current_note.status = new_status
        current_session.commit()
        print(f"Статус заметки '{note_name}' обновлен на '{new_status}'.")

    except Exception as e:
        print(f"Ошибка при обновлении статуса заметки: {e}")

    finally:
        current_session.close()


def delete_note(current_session, username: str, note_name: str) -> None:
    try:
        current_note = current_user_info(current_session, username, note_name)

        if not current_note:
            print(f"Заметка с названием {note_name} не найдена у пользователя {username}.")
            return

        current_session.delete(current_note)
        current_session.commit()
        print(f"Заметка '{note_name}' удалена у пользователя {username}.")

    except Exception as e:
        print(f"Ошибка при удалении заметки: {e}")

    finally:
        session.close()


def delete_user(current_session, username: str) -> bool:
    current_user = current_session.query(User).filter(User.username == username).first()

    if not current_user:
        print(f"Пользователь '{username}' не найден.")
        return False

    try:
        current_session.delete(current_user)
        current_session.commit()
        print(f"Пользователь '{username}' Был успешно удален.")
        return True
    except IntegrityError as e:
        current_session.rollback()
        print(f"Ошибка при удалении '{username}': {e}")
        return False


if __name__ == "__main__":
    # Инициализация и подключение к базе данных
    init_db()
    session = SessionLocal()

    # Пример добавления имени и заметки
    user = create_user(session, "Johan")
    print(f"Пользователь создан: \n{user}")

    note = create_note(
        session, username="Johan", title="workout", content="chest day",
        status="waiting", issue_date="2025-Jan-10",
    )
    print(f"Заметка создана:\n{note}")

    # Пример просмотра заметки
    get_note(session, username="Johan")

    # Пример обновления статуса заметки
    # update_note_status(session, username="Johan", note_name="workout", new_status="done.")

    # Пример удаления
    # delete_note(session, "Johan", "workout")

    # Пример удаления пользователя и его заметок (если они есть)
    # delete_user(session, "Johan")
