Бот нужен для хранения и удобного доступа изо всех дочерних чатов к одному source of truth
qasistersFirstBot

У бота должно есть 2 категории юзеров - админы и все остальные. 
Админство должно проверяться по состоянию в админском чате. 
Для любого вызывающего должно проверяться его состояние в основном чате.

TELEGRAM_API_TOKEN — API токен бота 
CHAT_ID = айди основного чата
ADMIN_CHAT_ID = айди админского чата

Использование с Docker показано ниже. Предварительно заполните ENV переменные, указанные выше, 
в Dockerfile, а также в команде запуска полностью укажите локальную директорию с проектом вместо local_project_path. 
SQLite база данных будет лежать в папке проекта db/qa_rules.db.

docker build -t tgsis ./
docker run -d --name tg -v /local_project_path/db:/home/db tgsis
Чтобы войти в работающий контейнер:

docker exec -ti tg bash
Войти в контейнере в SQL шелл:

docker exec -ti tg bash
sqlite3 /home/db/qa_rules.db