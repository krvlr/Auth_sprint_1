# Проектная работа 6 спринта
---

https://github.com/krvlr/Auth_sprint_1

В рамках данного репозитория реализованы следующие сервисы:

- Сервис авторизации

## Описание структуры репозитория:
---

1. `db` — раздел с настройками базы `PostgreSQL`.
2. `flask-auth` — раздел с описанием сервиса авторизации.
3. `nginx` — раздел с описанием настроек `nginx` для сервиса авторизации.

## Пример запуска
---

Перед запуском контейнеров, в корне `/` необходимо создать файл `.env` (в качестве примера `.env.example`):

    touch .env

А также указать в нем значения следующих переменных окружения:

    AUTH_DB_HOST
    AUTH_DB_PORT
    AUTH_DB_NAME
    AUTH_DB_USER
    AUTH_DB_PASSWORD
    AUTH_REDIS_HOST
    AUTH_REDIS_PORT
    JWT_COOKIE_SECURE
    JWT_TOKEN_LOCATION
    JWT_SECRET_KEY
    JWT_ACCESS_TOKEN_EXPIRES
    JWT_REFRESH_TOKEN_EXPIRES
    LOGGING_LEVEL
    LOG_FORMAT

Теперь можно запустить сборку образа и запуск контейнеров:

    docker compose up -d --build

Чтобы остановить и полностью удалить контейнеры со всеми `volume` и `network`, описанными в рамках `docker-compose.yml`:

    docker-compose down --rmi all -v --remove-orphans

## Миграции
---

Первым шагом необходимо перейти в дирректорию c точкой входа (`main.py`):

    cd /flask-auth/src/

Для генерации миграций структуры таблиц, описание которых находится в дирректории `/flask-auth/src/db/models` необходимо выполнить следующую команду:
    
    flask --app main db migrate -m "Описание миграции"

Для применения сформированной миграции необхожимо выполнить следующую команду:
    
    flask --app main db upgrade

## Тестирование
---

Для запуска тестирования необходимо перейти в папку с тестами:

    cd flask-auth/tests/functional/

И запустить сборку образа и запуск контейнеров для тестирования:

    docker compose up --build

Если в логах будет сообщение об успешном прохождении тестирования - значит пришел успех!

## Настройка flake8 и pre-commit hook
---

Сформируем виртуальное `Python`-окружение в корне:

    python3 -m venv env

Активируем сформированное виртуальное `Python`-окружение:

    . env/bin/activate

Обновим `pip`:

    pip install --upgrade pip

Установим зависимости проекта:

    pip install -r requirements.txt

Установим `pre-commit hook`:

    pre-commit install

