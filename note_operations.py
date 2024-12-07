from utils.date_validator import format_date, compare_dates
from models.note import Note
from models.user import User
from user_operations import current_user_info


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

    allowed_statuses = {"В ожидании", "Готово", "Отложено", "Просрочено"}
    if status not in allowed_statuses:
        raise ValueError(f"Недопустимый статус: {status}. Возможные значения: {', '.join(allowed_statuses)}")

    issue_date = format_date(issue_date)
    comment = compare_dates(issue_date, status)

    current_note = Note(
        title=title,
        content=content,
        status=status,
        issue_date=issue_date,
        comment=comment,
        user_id=current_user.id,
    )

    current_session.add(current_note)
    current_session.commit()
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
            print(f"Комментарий: {one_note.comment}")
            print("-" * 40)

        return notes

    except Exception as e:
        print(f"Ошибка при получении заметок: {e}")
        return []

    finally:
        current_session.close()


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
        current_session.close()