from sqlalchemy.exc import IntegrityError

from database.db import init_db, SessionLocal
from models.note import Note
from models.user import User


def create_user(current_session, username) -> None | User:
    new_user = User(username=username)
    try:
        current_session.add(new_user)
        current_session.commit()
        print(f"User '{username}' created successfully!")
    except IntegrityError:
        current_session.rollback()
        print(f"User '{username}' already exists.")
    return user


def create_note(
        current_session,
        username,
        title,
        content,
        status,
        issue_date,
) -> Note | None:
    cur_user = current_session.query(User).filter(User.username == username).first()
    if not cur_user:
        print(f"User '{username}' not found.")
        return None

    cur_note = Note(
        title=title,
        content=content,
        status=status,
        issue_date=issue_date,
        user_id=cur_user.id,
    )
    session.add(cur_note)
    session.commit()
    print(f"Note '{title}' added for user '{username}'.")
    return note


if __name__ == "__main__":
    init_db()
    session = SessionLocal()
    user = create_user(session, "")
    print(f"Пользователь создан: {user}")

    note = create_note(session, "")
    print(f"Заметка создана:\n{note}")

