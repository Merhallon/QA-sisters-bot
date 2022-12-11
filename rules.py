""" Работа с новыми правилами"""
import db

from typing import NamedTuple, Optional, List


class Rules(NamedTuple):
    """Структура добавленного в БД правила"""
    id: Optional[int]
    rules_text: str


def add_rules(raw_message: str) -> Rules:
    """Добавляет новое сообщение.
    Принимает на вход текст сообщения, пришедшего в бот."""
    # инсерт в sqllite базу
    db.insert("rules", {
        "raw_text": raw_message
    })
    return Rules(id=None, rules_text=raw_message)


def get_all_rules_from_bd() -> List[Rules]:
    """Возвращает строкой все правила из бд"""
    cursor = db.get_cursor()
    cursor.execute(
        'select * from rules'
    )
    results = cursor.fetchall()
    rules = [Rules(id=result[0], rules_text=result[1]) for result in results]
    return rules

