# Task Management API

RESTful API для управления задачами с JWT-аутентификацией.

## Стек
- FastAPI
- SQLAlchemy (SQLite)
- JWT (python-jose)
- Pytest
- Docker

## Функциональность
- Регистрация / вход
- CRUD для задач
- Фильтрация по статусу
- Пагинация
- Комментарии к задачам
- Роли: пользователь и администратор

## Запуск

### Локально
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
