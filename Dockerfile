FROM python:3.9

WORKDIR /home

ENV TELEGRAM_API_TOKEN = ''
ENV CHAT_ID = ''
ENV ADMIN_CHAT_ID = ''

RUN pip install -U pip aiogram pytz && apt-get update && apt-get install sqlite3
COPY *.py ./
COPY createdb.sql ./

ENTRYPOINT ["python", "bot.py"]