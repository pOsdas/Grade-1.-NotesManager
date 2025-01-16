from datetime import datetime

from note_operations import create_note, get_note, delete_note
from database.db import init_db, SessionLocal


init_db()
current_session = SessionLocal()
issue_date = datetime.strptime("2025-02-16", "%Y-%m-%d")


def test_create_note():
    # Тест на создание заметки без пользователя
    create_note(current_session, "test_user", "Test title", "something", "В ожидании", issue_date)
    assert "'test_user' не найден"


def test_get_note():
    # Тест на получение заметок без пользователя
    fetched_note = get_note(current_session, "test_user")
    assert fetched_note == []
