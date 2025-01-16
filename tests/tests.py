import unittest
from datetime import datetime

from note_operations import create_note, get_note
from user_operations import create_user, delete_user
from utils.date_validator import format_date
from database.db import init_db, SessionLocal


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Инициализация базы данных
        init_db()
        cls.session = SessionLocal()
        cls.issue_date = datetime.strptime("2025-02-16", "%Y-%m-%d")
        

class TestNoteOperations(BaseTest):
    def test_create_note_without_user(self):
        # Тест на создание заметки без пользователя
        note = create_note(self.session, "test_user", "Test title", "something", "В ожидании", self.issue_date)
        self.assertEqual(note, None)

    def test_get_note_without_user(self):
        # Тест на получение заметок без пользователя
        fetched_note = get_note(self.session, "test_user")
        self.assertEqual(fetched_note, [])


class TestUserOperations(BaseTest):
    def test_create_user(self):
        # Тест на создание пользователя
        user = create_user(self.session, "test_user")
        self.assertEqual(user.username, "test_user")
        self.assertIsNotNone(user.id)

    def test_delete_user(self):
        # Тест на удаление пользователя
        result = delete_user(self.session, "test_user")
        self.assertTrue(result)


class TestDateValidator(BaseTest):
    def test_format_date_valid(self):
        # Проверяем корректный формат
        result = format_date("2025/12/14")
        self.assertEqual(result, datetime(2025, 12, 14, 0, 0))

    def test_format_date_invalid(self):
        # Проверяем некорректный формат
        with self.assertRaises(ValueError) as context:
            format_date("2025^^12^^14")
        self.assertEqual(str(context.exception), "Формат даты не поддерживается: 2025^^12^^14")
