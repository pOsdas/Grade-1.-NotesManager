from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from colorama import Fore
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from utils.date_validator import compare_dates, format_date
from utils.status import check_status, display_note_status
from models.note import Note
from models.user import User
from user_operations import current_user_info


def create_note(
        current_session,
        username: str,
        title: str,
        content: str,
        status: str,
        issue_date: datetime,
) -> Note | None:
    """
    Создание заметки.
    """

    current_user = current_session.query(User).filter(User.username == username).first()
    if not current_user:
        print(f"Пользователь '{username}' не найден. ⚠️")
        return None

    comment = compare_dates(issue_date, status)

    current_note = Note(
        title=title,
        content=content,
        status=status,
        issue_date=issue_date,
        comment=comment,
        user_id=current_user.id,
    )

    current_session.add(current_note)
    current_session.commit()
    print(f"Заметка '{title}' добавлена для пользователя '{username}'. ✅")
    return current_note


def get_notes(current_session, username: str) -> list:
    """
    Вывод всех заметок для пользователя.
    """
    try:
        current_user = current_session.query(User).filter_by(username=username).first()
        if not current_user:
            print(f"Пользователь с именем {username} не найден. ⚠️")
            return []
        notes = current_session.query(Note).filter_by(user_id=current_user.id).all()
        if not notes:
            print(f"У пользователя {username} нет заметок. ⚠️")
            return []

        print(f"Заметки пользователя {username}:")
        print("-" * 40)
        # Выводим каждую заметку
        for one_note in notes:
            print(f"Заголовок: {one_note.title}")
            print(f"Содержание: {one_note.content}")
            print(f"Статус: {display_note_status(one_note.status)}")
            print(f"Дата создания: {one_note.created_date}")
            print(f"Дата завершения: {one_note.issue_date}")
            print(f"Комментарий: {one_note.comment}")
            print("-" * 40)

        return notes

    except Exception as e:
        print(f"Ошибка при получении заметок: {e} ❌")
        return []

    finally:
        current_session.close()


def display_notes_paginated(current_session) -> str | None:
    """
    Функция для постраничного отображения заметок.
    Каждая страница содержит до 3 заметок.
    """
    notes = current_session.query(Note).all()

    if not notes:
        print("Нет заметок для отображения. ⚠️")
        return

    page_size = 3  # Количество заметок на одной странице
    current_page = 0  # Индекс текущей страницы

    while True:
        start_index = current_page * page_size
        end_index = start_index + page_size
        page_notes = notes[start_index:end_index]

        if not page_notes:
            print("Страница пуста. ⚠️")
            break

        print(f"\n=== Страница {current_page + 1}/{(len(notes) + page_size - 1) // page_size} ===")
        for index, note in enumerate(page_notes, start=start_index + 1):
            print(f"{index}. {note.title} — {display_note_status(note.status)} — {note.issue_date}")

        print("\n[N] — Следующая страница.")
        print("[P] — Предыдущая страница.")
        print("[Q] — Выход.")

        choice = input("Выберите действие: ").strip().upper()

        if choice == "N":
            if end_index >= len(notes):
                print("Это последняя страница. ⚠️")
            else:
                current_page += 1
        elif choice == "P":
            if current_page == 0:
                print("Это первая страница. ⚠️")
            else:
                current_page -= 1
        elif choice == "Q":
            print("Выход из режима просмотра. 👋")
            break
        else:
            print("Некорректный ввод. Попробуйте снова. ❌")


def update_note_status(current_session, username: str, note_name: str, new_status: str) -> None:
    """
    Изменение статуса заметки.
    """
    try:
        current_note = current_user_info(current_session, username, note_name)

        if not current_note:
            print(f"Заметка с названием {note_name} не найдена у пользователя {username}. ⚠️")
            return

        current_note.status = new_status
        current_session.commit()
        print(f"Статус заметки '{note_name}' обновлен на '{display_note_status(new_status)}'. ✅")

    except Exception as e:
        print(f"Ошибка при обновлении статуса заметки: {e} ❌")

    finally:
        current_session.close()


def check_reminders(current_session) -> None:
    """
    Проверяет все заметки на наличие истёкших дедлайнов и выводит напоминания.
    """
    try:
        # Загрузка всех заметок
        notes = current_session.query(Note).all()
        if not notes:
            print("Нет заметок в базе данных. ⚠️")
            return

        reminders = []
        current_date = datetime.now()

        # Проверка дедлайнов
        for note in notes:
            issue_date = note.issue_date
            if issue_date < current_date:
                reminders.append(note)

        # Вывод напоминаний
        if reminders:
            print("\n=== Напоминания ===\n")
            for note in reminders:
                print(f"Заметка: {note.title}")
                print(f"Дедлайн: {note.issue_date} (истёк)\n")
        else:
            print("\n=== Напоминания ===\n")
            print("Напоминание: Нет истёкших дедлайнов. ✅")

    except Exception as e:
        print(f"Ошибка при проверке напоминаний: {e} ❌")

    finally:
        current_session.close()


def edit_note(current_session, username: str) -> None:
    """
    Изменение любого поля заметки.
    """
    current_user = current_session.query(User).filter_by(username=username).first()
    if not current_user:
        print(f"Пользователь с именем {username} не найден. ⚠️")
        return

    notes = current_session.query(Note).filter_by(user_id=current_user.id).all()
    if not notes:
        print(f"У пользователя {username} нет заметок. ⚠️")
        return

    print(f"Заметки пользователя {username}:")
    for index, note in enumerate(notes, start=1):
        print(f"{index}. {note.title}")

    try:
        note_number = int(input("Введите номер заметки для редактирования: "))
        if note_number < 1 or note_number > len(notes):
            print("Некорректный номер заметки. ⚠️")
            return
    except ValueError:
        print("Введите корректное число.")
        return

    selected_note = notes[note_number - 1]
    print(f"Вы выбрали заметку: {selected_note.title}")

    fields = {
        "title": "Заголовок:",
        "content": "Содержание:",
        "status": "Статус:",
        "issue_date": "Дата завершения (в формате ГГГГ-ММ-ДД):",
    }

    for field, description in fields.items():
        # status field
        if field == "status":
            current_value = getattr(selected_note, field)
            while True:
                new_value = input(f"{description} (текущее значение: {display_note_status(current_value)}) "
                                  f"(оставьте пустым для пропуска): ")
                if not new_value.strip():
                    break
                try:
                    check_status(new_value)
                    setattr(selected_note, field, new_value.strip())
                    break
                except ValueError as e:
                    print(e, "❌")

        # issue_date field
        elif field == "issue_date":
            current_value = getattr(selected_note, field)
            while True:
                new_value = input(f"{description} (текущее значение: {current_value}) (оставьте пустым для пропуска): ")
                if not new_value.strip():
                    break
                try:
                    parsed_date = format_date(new_value)
                    setattr(selected_note, field, parsed_date)
                    break
                except ValueError as e:
                    print(e, "❌")

        # other fields
        else:
            current_value = getattr(selected_note, field)
            new_value = input(f"{description} (текущее значение: {current_value}) (оставьте пустым для пропуска): ")
            if new_value.strip():
                setattr(selected_note, field, new_value.strip())

    try:
        current_session.commit()
        print(Fore.GREEN + "Успех" + "✅")
    except SQLAlchemyError as e:
        current_session.rollback()
        print(f"Ошибка при сохранении изменений: {e} ❌")


def search_notes(session, keyword: str = "", status: str = ""):
    """
    Производит поиск заметок в базе данных.
    """
    query = session.query(Note)

    if keyword:
        query = query.filter(
            (Note.title.contains(keyword)) | (Note.content.contains(keyword))
        )

    if status:
        query = query.filter(Note.status == status)

    results = query.all()

    if results:
        print("Найденные заметки:")
        for note in results:
            print(f"Заголовок: {note.title}, Статус: {display_note_status(note.status)}, Содержание: {note.content}")
    else:
        print("Нет заметок, соответствующих критериям поиска. ⚠️")


def filter_notes(current_session, filter_type: int, filter_value: str) -> list:
    """
    Фильтрует заметки пользователя из базы данных.
    """
    query = current_session.query(Note)

    # По ключевому слову
    if filter_type == 1:
        return query.filter(Note.title.ilike(f"%{filter_value}%") | Note.content.ilike(f"%{filter_value}%")).all()
    # По статусу
    elif filter_type == 2:
        return query.filter(Note.status.ilike(filter_value)).all()
    # По дате
    elif filter_type == 3:
        try:
            filter_date = datetime.strptime(filter_value, "%Y-%m-%d")
            return query.filter(Note.issue_date == filter_date).all()
        except ValueError:
            print("Ошибка: Некорректный формат даты. ⚠️")
            return []
    else:
        print("Ошибка: Некорректный тип фильтра. ⚠️")
        return []


def export_notes_to_file(current_session, export_format: str) -> bool | None:
    """
    Экспортирует все заметки в .txt или .pdf файл.
    """
    notes = current_session.query(Note).all()
    if not notes:
        print("Нет заметок для экспорта. ⚠️")
        return

    # В текстовый файл
    if export_format.lower() == "txt":
        try:
            file_path = "../exports/notes_export.txt"
            with open(file_path, "w", encoding="utf-8") as file:
                for note in notes:
                    file.write(f"Заголовок: {note.title}\n")
                    file.write(f"Содержание: {note.content}\n")
                    file.write(f"Статус: {note.status}\n")
                    file.write(f"Дата создания: {note.created_date}\n")
                    file.write(f"Дедлайн: {note.issue_date}\n")
                    file.write("=" * 50 + "\n")
            print(f"Заметки успешно экспортированы в {file_path} ✅")
            return True

        except Exception as e:
            print(f"Ошибка при экспорте в TXT: {e} ❌")

    # В pdf
    elif export_format.lower() == "pdf":
        file_path = "../exports/notes_export.pdf"
        try:
            pdf = canvas.Canvas(file_path, pagesize=A4)
            width, height = A4
            margin = 40
            y_position = height - margin

            # Заголовок документа
            pdfmetrics.registerFont(TTFont('ArialBold', 'arialbd.ttf'))
            pdf.setFont("ArialBold", 16)
            pdf.drawString(margin, y_position, "Список заметок")
            y_position -= 30

            # Основной контент
            pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
            pdf.setFont("Arial", 12)
            for note in notes:
                if y_position < margin:
                    pdf.showPage()
                    y_position = height - margin

                # Добавляем информацию о заметке
                pdf.drawString(margin, y_position, f"Заголовок: {note.title}")
                y_position -= 15
                pdf.drawString(margin, y_position, f"Содержание: {note.content}")
                y_position -= 15
                pdf.drawString(margin, y_position, f"Статус: {note.status}")
                y_position -= 15
                pdf.drawString(margin, y_position, f"Комментарий: {note.comment}")
                y_position -= 15
                pdf.drawString(margin, y_position, f"Дата создания: {note.created_date}")
                y_position -= 15
                pdf.drawString(margin, y_position, f"Дата завершения: {note.issue_date}")
                y_position -= 30

            pdf.save()
            print(f"Заметки успешно экспортированы в PDF: {file_path} ✅")
            return True

        except Exception as e:
            print(f"Ошибка при экспорте в PDF: {e} ❌")

    else:
        return False


def delete_note(current_session, username: str, note_name: str) -> None:
    """
    Удаляет заметку из базы данных.
    """
    try:
        current_note = current_user_info(current_session, username, note_name)

        if not current_note:
            print(f"Заметка с названием {note_name} не найдена у пользователя {username}. ⚠️")
            return

        current_session.delete(current_note)
        current_session.commit()
        print(f"Заметка '{note_name}' удалена у пользователя {username}. ✅")

    except Exception as e:
        print(f"Ошибка при удалении заметки: {e} ❌")

    finally:
        current_session.close()
