from sqlalchemy.exc import IntegrityError
from models.user import User
from models.note import Note


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


def current_user_info(current_session, username: str, note_name: str) -> Note | None:
    current_user = current_session.query(User).filter_by(username=username).first()

    if not current_user:
        print(f"Пользователь с именем {username} не найден.")
        return

    note_info = current_session.query(Note).filter_by(title=note_name, user_id=current_user.id).first()
    return note_info


def get_user_notes_titles(current_session, username: str) -> tuple[list[str], int]:
    current_user = current_session.query(User).filter_by(username=username).first()
    bool_var = 1

    if not current_user:
        bool_var = 0
        return [], bool_var

    notes = current_session.query(Note).filter_by(user_id=current_user.id).all()

    if not notes:
        bool_var = 0
        return [], bool_var

    return [note.title for note in notes], bool_var


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
