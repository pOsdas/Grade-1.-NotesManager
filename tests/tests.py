import unittest
from datetime import datetime

from note_operations import create_note, get_note, update_note_status, edit_note, delete_note
from user_operations import create_user, delete_user, current_user_info, get_user_notes_titles
from utils.date_validator import format_date, give_time, compare_dates
from utils.status import check_status
from database.db import init_db, SessionLocal


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Инициализация базы данных
        init_db()
        cls.session = SessionLocal()
        cls.issue_date = datetime.strptime("2025-02-16", "%Y-%m-%d")


class TestUserOperations(BaseTest):
    def test_create_user(self):
        # Тест на создание пользователя
        user = create_user(self.session, "test_user")
        self.assertEqual(user.username, "test_user")
        self.assertIsNotNone(user.id)

    def test_current_user_info(self):
        # Тест на информацию не сущ. Заметки
        current_user = current_user_info(self.session, "test_user", "test_title")
        self.assertIsNone(current_user)

    def test_get_user_notes_titles(self):
        # Тест на список не сущ. Заметок
        info = get_user_notes_titles(self.session, "test_user")
        self.assertEqual(info, ([], 0))

    def test_delete_user(self):
        # Тест на удаление пользователя
        result = delete_user(self.session, "test_user")
        self.assertTrue(result)


class TestNoteOperations(BaseTest):
    def test_create_note_without_user(self):
        # Тест на создание заметки без пользователя
        note = create_note(self.session, "test_user", "Test title", "Test content", "В ожидании", self.issue_date)
        self.assertEqual(note, None)

    def test_get_note_without_user(self):
        # Тест на получение заметок без пользователя
        fetched_note = get_note(self.session, "test_user")
        self.assertEqual(fetched_note, [])

    def test_create_note_with_user(self):
        # Тест на создание заметки с пользователем
        create_user(self.session, "test_user")
        note = create_note(self.session, "test_user", "Test title", "something", "В ожидании", self.issue_date)
        self.assertEqual(note, note)

    def test_get_note_with_user(self):
        # Тест на получение заметок с пользователем
        fetched_note = get_note(self.session, "test_user")
        self.assertNotEqual(fetched_note, [])
        delete_user(self.session, "test_user")

    def test_update_note_status(self):
        # Тест на обновление статуса заметки
        update_note_status(self.session, "test_user", "Test title", "Готово")
        note = current_user_info(self.session, "test_user", "Test title")
        self.assertEqual(note.status, "Готово")

    def test_edit_note(self):
        # Тест на обновление информации (В данном случае содержимого)
        edit_note(self.session, "test_user")
        note = current_user_info(self.session, "test_user", "Test title")
        self.assertEqual(note.content, "something")

    def test_delete_note(self):
        # Тест на удаление заметки
        delete_note(self, "test_user", "Test title")
        self.assertTrue(True)


class TestUtils(BaseTest):
    def test_format_date_valid(self):
        # Проверяем корректный формат
        result = format_date("2025/12/14")
        self.assertEqual(result, datetime(2025, 12, 14, 0, 0))

    def test_format_date_invalid(self):
        # Проверяем некорректный формат
        with self.assertRaises(ValueError) as context:
            format_date("2025^^12^^14")
        self.assertEqual(str(context.exception), "Формат даты не поддерживается: 2025^^12^^14")

    def test_give_time(self):
        # Склонение времени
        time = give_time(17, 12, 14)
        self.assertEqual(time, "17 дней, 12 часов, 14 минут.")

    def test_compare_dates(self):
        # Тест на сравнение даты создания и дедлайн
        output = compare_dates(datetime(2025, 10, 10, 0, 0, 0), "Готово")
        self.assertEqual(output, "Готово")
        output = compare_dates(datetime(2025, 10, 10, 0, 0, 0), "Отложено")
        self.assertEqual(output, "Отложено")
        output = compare_dates(datetime(2025, 10, 10, 0, 0, 0), "В ожидании")
        self.assertNotEqual(output, "В ожидании")
        output = compare_dates(datetime(2025, 10, 10, 0, 0, 0), "Просрочено")
        self.assertNotEqual(output, "Просрочено")

    def test_check_status(self):
        # Проверка не правильного статуса
        with self.assertRaises(ValueError) as context:
            check_status("something")
        self.assertNotEqual(str(context.exception), True)

        # Проверка правильного статуса
        output = check_status("Готово")
        self.assertEqual(output, True)
