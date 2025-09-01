# 📄 Resume Management App

> Современное веб-приложение для управления резюме с интеграцией ИИ

[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.3.4-4FC08D?logo=vue.js)](https://vuejs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql)](https://postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)](https://docker.com/)
[![Poetry](https://img.shields.io/badge/Poetry-1.6.1-blue?logo=poetry)](https://python-poetry.org/)

## 🚀 Особенности

### 🔐 Аутентификация
- Регистрация пользователей по email и паролю
- JWT токены для безопасной авторизации
- Защищенные маршруты

### 📝 Управление резюме
- **CRUD операции**: создание, чтение, обновление, удаление
- Список всех резюме пользователя
- Детальный просмотр резюме
- Структурированные поля: заголовок и содержание

### 🤖 ИИ интеграция
- Эндпоинт для улучшения резюме `/resume/{id}/improve`
- Заглушка для демонстрации (добавляет " [Improved]")
- История улучшений в базе данных
- Готовность к интеграции с реальными ИИ сервисами

### 🎨 Фронтенд
- Современный Vue.js интерфейс
- Адаптивный дизайн
- Интуитивная навигация
- Форма авторизации
- Управление резюме через UI

## 🛠 Технологический стек

### Backend
- **FastAPI** - современный Python веб-фреймворк
- **PostgreSQL** - надежная реляционная база данных
- **SQLAlchemy** - ORM для работы с БД
- **Alembic** - миграции базы данных
- **JWT** - безопасная аутентификация
- **Pytest** - тестирование

### Frontend
- **Vue.js 3** - прогрессивный JavaScript фреймворк
- **Vite** - быстрый сборщик
- **JavaScript ES6+** - современный JavaScript

### DevOps
- **Docker & Docker Compose** - контейнеризация
- **Poetry** - управление зависимостями Python
- **NPM** - управление пакетами Node.js

## 📁 Структура проекта

```
resume-management-app/
├── 🔧 backend/                 # FastAPI приложение
│   ├── 📊 alembic/            # Миграции БД
│   ├── 🐍 app/                # Исходный код
│   ├── 🧪 tests/              # Тесты
│   ├── 🐳 Dockerfile          # Docker конфиг
│   └── 📦 pyproject.toml      # Зависимости
├── 🎨 frontend/               # Vue.js приложение
│   ├── 📱 src/                # Исходный код
│   ├── 🌐 public/             # Статические файлы
│   ├── 🐳 Dockerfile          # Docker конфиг
│   └── 📋 package.json        # Зависимости
├── 🐳 docker-compose.yml      # Оркестрация
└── 📖 README.md              # Документация
```

## ⚡ Быстрый старт

### 🐳 С Docker (рекомендуется)

1. **Клонируйте репозиторий**
   ```bash
   git clone https://github.com/BahaGit2002/resume-fullproject
   cd resume-fullproject
   ```

2. **Настройте переменные окружения**
   ```bash
   cp backend/.env.example backend/.env
   # Отредактируйте .env файл
   ```

3. **Запустите приложение**
   ```bash
   docker-compose up --build
   ```

4. **Откройте в браузере**
    - 🎨 Фронтенд: http://localhost:8080
    - 🔧 API: http://localhost:8000
    - 📚 Документация: http://localhost:8000/docs

### 💻 Локальная разработка

<details>
<summary>Развернуть инструкции для локальной разработки</summary>

#### Backend
```bash
cd backend
poetry install
poetry shell
alembic upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend
```bash
cd frontend
npm install
npm run build
npm install -g serve
serve -s dist -l 8080
```

#### База данных
- PostgreSQL с настройками:
    - Пользователь: `root`
    - Пароль: `a!~A1H04;N"I`
    - База: `resume_db`

</details>

## 🔧 Переменные окружения

Создайте файл `.env` в папке `backend/`:

```env
# Database
DATABASE_URL=postgresql+asyncpg://root:password@localhost:5432/resume_db

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

BACKEND_CORS_ORIGINS='["http://127.0.0.1:5173", "http://localhost:5173", "http://localhost:8080", "http://127.0.0.1:8080"]'
```

> ⚠️ **Важно**: Никогда не коммитьте `.env` файлы в репозиторий!

## 📋 API Эндпоинты

### 🔐 Аутентификация
| Метод | Путь | Описание | Авторизация |
|-------|------|----------|-------------|
| `POST` | `/users/register` | Регистрация пользователя | ❌ |
| `POST` | `/users/login` | Вход в систему | ❌ |

### 📝 Резюме
| Метод    | Путь                           | Описание                | Авторизация |
|----------|--------------------------------|-------------------------|-------------|
| `POST`   | `/resumes/`                    | Создать резюме          | ✅ JWT |
| `GET`    | `/resumes/`                    | Список резюме           | ✅ JWT |
| `GET`    | `/resumes/{resume_id}`         | Получить резюме         | ✅ JWT |
| `PUT`    | `/resumes/{resume_id}`         | Обновить резюме         | ✅ JWT |
| `DELETE` | `/resumes/{resume_id}`         | Удалить резюме          | ✅ JWT |
| `POST`   | `/resumes/{resume_id}/improve` | Улучшить с ИИ           | ✅ JWT |
| `GET`    | `/resumes/{resume_id}/history` | Получить историю резюме | ✅ JWT |

> 📚 Полная документация API доступна на `/docs` после запуска бэкенда

## 🧪 Тестирование

### Запуск тестов
```bash
cd backend
poetry run pytest
```

### Покрытие кода
```bash
poetry run pytest --cov=app
```

### Просмотр отчета покрытия
```bash
poetry run pytest --cov=app --cov-report=html
# Откройте htmlcov/index.html в браузере
```

## 📄 Лицензия

Этот проект лицензирован под MIT License - см. файл [LICENSE](LICENSE) для деталей.

