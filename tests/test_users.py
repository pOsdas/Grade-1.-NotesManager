from user_operations import create_user, delete_user
from database.db import init_db, SessionLocal


init_db()
current_session = SessionLocal()


def test_create_user():
    # Тест на создание пользователя
    user = create_user(current_session, "test_user")
    assert user.username == "test_user"
    assert user.id is not None


def test_delete_user():
    # Тест на удаление пользователя
    result = delete_user(current_session, "test_user")
    assert result is True
