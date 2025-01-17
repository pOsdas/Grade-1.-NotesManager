from colorama import Fore, Style

from note_operations import filter_notes
from utils.status import display_note_status


def filters_menu(session):
    """
    Меню фильтрации заметок для пользователя.
    """
    print("\n=== Фильтры ===")
    print("1. По ключевому слову")
    print("2. По статусу")
    print("3. По дате")

    choice = input("Выберите фильтр (введите число): ")

    if choice == "1":
        keyword = input("Введите ключевое слово: ")
        filtered_notes = filter_notes(session, 1, filter_value=keyword)
    elif choice == "2":
        print(f"Доступные статусы: {Fore.YELLOW}В ожидании, {Fore.GREEN}Готово,"
              f" {Fore.LIGHTBLUE_EX}Отложено, {Fore.RED}Просрочено")
        status = input("Введите статус: ")
        filtered_notes = filter_notes(session, 2, filter_value=status)
    elif choice == "3":
        date = input("Введите дату (формат: ГГГГ-ММ-ДД): ")
        filtered_notes = filter_notes(session, 3, filter_value=date)
    else:
        print("Ошибка: Некорректный выбор фильтра. ❌")
        return

    if filtered_notes:
        print("\n=== Отфильтрованные заметки ===")
        for note in filtered_notes:
            print(f"Заголовок: {note.title}")
            print(f"Содержание: {note.content}")
            print(f"Статус: {display_note_status(note.status)}")
            print(f"Дата создания: {note.created_date}")
            print(f"Дата завершения: {note.issue_date}")
            print(f"Комментарий: {note.comment}")
            print("-" * 40)
    else:
        print("\nНет заметок, соответствующих фильтру. ⚠️")
