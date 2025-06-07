# Библиотечный API

REST API для управления библиотекой: регистрация и авторизация, учет читателей, выдача книг, возврат, отображение активных выдач.

**Технологии:** Python + FastAPI + SQLAlchemy + Alembic + SQLite + JWT

---

## Запуск проекта

```bash
git clone ...
cd project
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
python -m uvicorn Library.main:app --reload
```

Перейти на Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Аутентификация

Использовался JWT-токен. Аутентификация выполняется по OAuth2PasswordBearer.

**Эндпоинты:**

* `POST /register` — регистрация библиотекаря (username/email + password)
* `POST /login` — получение токена

**Защищёны:** все эндпоинты, связанные с доступом к учету книг и читателей.

**Библиотеки:**

* `python-jose` — для генерации и проверки JWT
* `passlib[bcrypt]` — хеширование паролей

---

## Структура базы данных

**Reader** — читатели

* id, name, email (уникальный), hashed\_password

**Book** — книги

* id, title, author, year, ISBN, num\_of\_books

**BorrowedBook** — журнал выдачи

* id, book\_id, reader\_id, borrow\_date, return\_date

> Идея: сделать отдельную таблицу BorrowedBook, чтобы учитывать историю выдач и возвратов

---

## Бизнес-логика: пункты 4.1, 4.2, 4.3

### 4.1 Выдача книги

* Книгу нельзя выдать, если `num_of_books == 0`
* Читателю нельзя выдать более 3 книг
* Сохраняется BorrowedBook с NULL return\_date

### 4.2 Возврат книги

* По `borrow_id` ищется выдача
* Если return\_date уже есть — выдается 400
* Увеличивается num\_of\_books, запись обновляет return\_date

### 4.3 Проверка активных выдач

* Список активных BorrowedBook c `return_date is NULL`
* Добавлено вывод инфо о книге (title, author, date)

**Сложности:** сразу не сработали ограничения на 3 книги — решил через `.count()` и фильтр по `return_date is None`

---

## Дополнительная идея

Фильтр и поиск книг по автору/году/ISBN

Можно добавить параметры в `GET /books/`, например:

```url
/books/?author=Толстой&year=1869
```

Фильтрация через SQLAlchemy `.filter()` по переданным параметрам.

---

## Автор

Разработано в рамках тестового задания для стажировки.
Немало что я делал впервые, так что пришлось много гуглить и искать красивые решения задач, и учиться применять их в деле. Думаю, получилось хорошо.
