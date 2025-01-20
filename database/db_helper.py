from sqlalchemy.sql import text
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = 'sqlite:///../notes_manager.db'  # на два уровня выше (осторожнее при изменении пути в config.py)

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

session = SessionLocal()


# Просмотреть структуру таблицы
def inspect_notes_table():
    try:
        result = session.execute(text("PRAGMA table_info(notes)")).fetchall()
        print("Структура таблицы notes:")
        for row in result:
            print(row)
    except Exception as e:
        print(f"Ошибка при проверке структуры таблицы: {e} ❌")
    finally:
        session.close()


# Получить все заметки
def fetch_all_notes_raw():
    try:
        result = session.execute(text("SELECT * FROM notes")).fetchall()
        if result:
            print("Содержимое таблицы notes:")
            for row in result:
                print(row)
        else:
            print("Таблица notes пуста. ⚠️")
    except Exception as e:
        print(f"Ошибка при выполнении запроса: {e} ❌")
    finally:
        session.close()


# inspect_notes_table()
fetch_all_notes_raw()
