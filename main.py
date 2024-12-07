from database.db import init_db, SessionLocal
from user_operations import create_user, current_user_info, delete_user
from note_operations import create_note, get_note, update_note_status, delete_note

if __name__ == "__main__":
    # Инициализация и подключение к базе данных
    init_db()
    session = SessionLocal()

    # Пример добавления имени и заметки
    # user = create_user(session, "Ilya")
    # print(f"Пользователь создан: \n{user}")

    note = create_note(
        session, username="Ilya", title="cook curry", content="buy ingredients",
        status="В ожидании", issue_date="2024-Dec-8",
    )
    print(f"Заметка создана:\n{note}")

    # Пример просмотра заметки
    # get_note(session, username="Johan")

    # Пример обновления статуса заметки
    # update_note_status(session, username="Johan", note_name="workout", new_status="done.")

    # Пример удаления
    # delete_note(session, "Ilya", "cook curry")

    # Пример удаления пользователя и его заметок (если они есть)
    # delete_user(session, "Johan")
