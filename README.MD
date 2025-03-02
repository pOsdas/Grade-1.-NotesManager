# NotesManager
## 📖 Описание проекта 
NotesManager — это приложение для управления заметками и задачами, разработанное на Python с использованием библиотеки SQLAlchemy для работы с базой данных. Проект предоставляет удобный способ создания, обновления, удаления и управления заметками, привязанными к пользователям.

---
## Содержание
- [Libraries](#Libraries)
- [Project structure](#Project-structure)
- [Running](#Running)
  - [For windows](#Windows)
  - [For Linux](#Linux)
- [Usage](#Usage) 
- [License](#License)
- [Author](#Author)
---
## Libraries
* SQLAlchemy
* datetime
* typing_extensions
* greenlet
* colorama
* reportlab

## Project structure

```
├── database                    # Работа с базой данных
│   ├── __init__.py             # Инициализация модуля database
│   ├── db.py                   # Подключение к базе данных
│   └── db_helper.py            # Хелперы для работы с БД
├── interface                   # Интерфейс взаимодействия с пользователем
│   ├── __init__.py             # Инициализация модуля interface
│   ├── additional_menu.py      # Меню фильтрации
│   └── menu.py                 # Основное меню
├── models                      # Описание моделей данных
│   ├── __init__.py             # Инициализация модуля models
│   ├── base.py                 # Базовый класс для декларативных моделей SQLAlchemy
│   ├── note.py                 # Модель заметки
│   └── user.py                 # Модель пользователя
├── tests                       # Модуль тестов
│   ├── __init__.py             # Инициализация модуля tests (не обязательно)
│   └── tests.py                # Тесты для проекта
├── utils                       # Утилиты и вспомогательные функции
│   ├── __init__.py             # Инициализация модуля utils
│   ├── date_validator.py       # Форматирование дат и работа с датами
│   ├── declension_of_words.py  # Склонение слов
│   └── status.py               # Проверка и окраска статусов
├── .dockerignore               # Исключения для Docker
├── .gitignore                  # Исключения для Git
├── config.py                   # Файл конфигурации
├── Dockerfile                  # Конфигурация Docker
├── LICENSE.txt                 # Лицензия проекта
├── main.py                     # Точка входа приложения
├── note_operations.py          # Операции связанные с заметками
├── README.MD                   # Документация проекта
├── requirements.py             # Зависимости проекта
└── user_operations.py          # Операции связанные с пользователями
```

## Running
Используйте `Dockerfile`, или:
1. Скопируйте репозиторий
```sh
git clone https://github.com/pOsdas/Grade-1.-NotesManager.git
cd [ваше имя]
```
2. Создайте и активируйте свою виртуальную среду 
    ### Windows:
    ```sh
    python -m venv venv
    source venv/Scripts/activate
    ```
    ### Linux/MacOS:
    ```sh
    python -m venv venv
    source venv/bin/activate
    ```

## Usage

1. Установить зависимости:
```commandline
pip install -r requirements.txt
```

## License
Распространяется под лицензией MIT.\
Дополнительная информация в файле `LICENSE.txt`.

## Author
Автор: pOsdas
