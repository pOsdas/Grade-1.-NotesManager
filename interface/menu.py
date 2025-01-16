from database.db import init_db, SessionLocal
from user_operations import (
    create_user, current_user_info,
    delete_user, get_user_notes_titles,
)
from note_operations import (
    create_note, get_note, update_note_status,
    delete_note, edit_note, search_notes,
)
from utils.date_validator import compare_dates, format_date
from utils.status import check_status

import sys


def main_menu():
    """
    Главное меню программы.
    """
    print("\n=== Главное меню ===")
    print("1. Добавить пользователя")
    print("2. Добавить заметку пользователю")
    print("3. Удалить заметку")
    print("4. Просмотреть заметки")
    print("5. Обновить информацию заметки")
    print("6. Обновить статус заметки")
    print("7. Проверить статус дедлайна заметки")
    print("8. Поиск по заметкам")
    print("9. Удалить пользователя и его заметки")
    print("10. Завершить программу")


def select_action():
    try:
        return int(input("Выберите действие (1-10): "))
    except ValueError:
        print("Пожалуйста, введите число от 1 до 10.")
        return None


def update_status_menu():
    print("\n=== Возможные статусы заметки ===")
    print("1. В ожидании")
    print("2. Готово")
    print("3. Отложено")
    print("4. Просрочено")
    while True:
        status_choice = input("Введите статус: ")
        try:
            check_status(status_choice)
            break
        except ValueError as e:
            print(e)

    return status_choice


def main():
    # Инициализация базы данных и сессии
    init_db()
    session = SessionLocal()

    while True:
        main_menu()
        choice = select_action()

        # Добавление пользователя
        if choice == 1:
            username = input("Введите имя пользователя: ")
            user = create_user(session, username)
            print(f"Пользователь создан: {user}")

        # Добавление заметки
        elif choice == 2:
            username = input("Введите имя пользователя: ")
            while True:
                title = input("Введите название заметки: ")
                content = input("Введите содержание заметки: ")
                while True:
                    status = input("Введите статус заметки: ")
                    try:
                        check_status(status)
                        break
                    except ValueError as e:
                        print(e)

                while True:
                    issue_date = input("Введите дату завершения заметки (в формате YYYY-MM-DD): ")
                    try:
                        issue_date = format_date(issue_date)
                        break
                    except ValueError as e:
                        print(e)

                note = create_note(session, username, title, content, status, issue_date)
                print(f"Заметка создана: {note}")

                another_note = input("Хотите создать еще одну заметку? (да/нет): ").strip().lower()
                if another_note != "да":
                    break

        # Удаление заметки
        elif choice == 3:
            username = input("Введите имя пользователя: ")
            titles, bool_varchar = get_user_notes_titles(session, username)
            if bool_varchar:
                print(f"Заметки: {titles}")
                note_name = input("Введите название заметки: ")
                delete_note(session, username, note_name)
            else:
                print(f"У пользователя {username} нет заметок!")

        # Просмотр заметки
        elif choice == 4:
            username = input("Введите имя пользователя: ")
            note = get_note(session, username)
            if note:
                print(note)

        # Обновить информацию заметки
        elif choice == 5:
            username = input("Введите имя пользователя: ")
            edit_note(session, username)

        # Обновление статуса заметки
        elif choice == 6:
            username = input("Введите имя пользователя: ")
            titles, bool_varchar = get_user_notes_titles(session, username)
            if bool_varchar:
                print(f"Заметки: {titles}")
                note_name = input("Введите название заметки: ")
                new_status = update_status_menu()
                if new_status:
                    update_note_status(session, username, note_name, new_status)
                else:
                    print("Неверный выбор статуса.")
            else:
                print(f"У пользователя {username} нет заметок!")

        # Проверка дедлайна
        elif choice == 7:
            username = input("Введите имя пользователя: ")
            titles, bool_varchar = get_user_notes_titles(session, username)
            if bool_varchar:
                print(f"Заметки: {titles}")
                note_name = input("Введите название заметки: ")
                note = current_user_info(session, username, note_name)
                if note:
                    comment = compare_dates(note.issue_date, note.status)
                    print(comment)
                else:
                    print("Заметка не найдена.")
            else:
                print(f"У пользователя {username} нет заметок!")

        # Поиск по заметкам
        elif choice == 8:
            keyword = input("Введите ключевое слово для поиска (или оставьте пустым): ")
            status = input("Введите статус для поиска (или оставьте пустым): ")
            search_notes(session, keyword=keyword, status=status)

        # Удаление пользователя и его заметок
        elif choice == 9:
            username = input("Введите имя пользователя: ")
            delete_user(session, username)

        # Завершение программы
        elif choice == 10:
            print("Программа завершена.")
            session.close()
            sys.exit()

        else:
            print("Неверный выбор. Пожалуйста, выберите действие из меню.")
