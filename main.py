from database.db import init_db, SessionLocal
from user_operations import create_user, current_user_info, delete_user, get_user_notes_titles
from note_operations import create_note, get_note, update_note_status, delete_note
from utils.date_validator import compare_dates

import sys


def main_menu():
    """
    Главное меню программы.
    """
    print("\n=== Главное меню ===")
    print("1. Добавить пользователя")
    print("2. Добавить заметку пользователю")
    print("3. Удалить заметку")
    print("4. Просмотреть заметку")
    print("5. Обновить статус заметки")
    print("6. Проверить статус дедлайна заметки")
    print("7. Удалить пользователя и его заметки")
    print("8. Завершить программу")


def select_action():
    try:
        return int(input("Выберите действие (1-8): "))
    except ValueError:
        print("Пожалуйста, введите число от 1 до 8.")
        return None


def update_status_menu():
    print("\n=== Возможные статусы заметки ===")
    print("1. В ожидании")
    print("2. Готово")
    print("3. Отложено")
    print("4. Просрочено")
    status_choice = input("Введите номер статуса (1-4): ")

    status_mapping = {
        "1": "В ожидании",
        "2": "Готово",
        "3": "Отложено",
        "4": "Просрочено",
    }

    return status_mapping.get(status_choice, None)


def main():
    # Инициализация базы данных и сессии
    init_db()
    session = SessionLocal()

    allowed_statuses = {"В ожидании", "Готово", "Отложено", "Просрочено"}

    while True:
        main_menu()
        choice = select_action()

        if choice == 1:
            # Добавление пользователя
            username = input("Введите имя пользователя: ")
            user = create_user(session, username)
            print(f"Пользователь создан: {user}")

        elif choice == 2:
            # Добавление заметки
            username = input("Введите имя пользователя: ")
            while True:
                title = input("Введите название заметки: ")
                content = input("Введите содержание заметки: ")
                status = input("Введите статус заметки (например: В ожидании, Готово, Отложено, Просрочено): ")
                if status not in allowed_statuses:
                    while status not in allowed_statuses:
                        print("Вы ввели недопустимый статус для заметки!")
                        status = input("Введите статус заметки (например, В ожидании, Готово, Отложеноб Просрочено): ")

                issue_date = input("Введите дату завершения заметки (в формате YYYY-MM-DD): ")

                note = create_note(session, username, title, content, status, issue_date)
                print(f"Заметка создана: {note}")

                another_note = input("Хотите создать еще одну заметку? (да/нет): ").strip().lower()
                if another_note != "да":
                    break

        elif choice == 3:
            # Удаление заметки
            username = input("Введите имя пользователя: ")
            titles, bool_varchar = get_user_notes_titles(session, username)
            if bool_varchar:
                print(f"Заметки: {titles}")
                note_name = input("Введите название заметки: ")
                delete_note(session, username, note_name)
            else:
                print(f"У пользователя {username} нет заметок!")

        elif choice == 4:
            # Просмотр заметки
            username = input("Введите имя пользователя: ")
            note = get_note(session, username)
            if note:
                print(note)

        elif choice == 5:
            # Обновление статуса заметки
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

        elif choice == 6:
            # Проверка дедлайна
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

        elif choice == 7:
            # Удаление пользователя и его заметок
            username = input("Введите имя пользователя: ")
            delete_user(session, username)

        elif choice == 8:
            # Завершение программы
            print("Программа завершена.")
            session.close()
            sys.exit()

        else:
            print("Неверный выбор. Пожалуйста, выберите действие из меню.")


if __name__ == "__main__":
    main()
