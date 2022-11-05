from enum import Enum

token = ''  # не будет здесь указан, тк github открытое пространство
db_file = "database.vdb"


class States(Enum):
    """
    Мы используем БД Vedis, в которой хранимые значения всегда строки,
    поэтому и тут будем использовать тоже строки (str)
    """
    S_START = "0"  # Начало нового диалога
    S_JOB = "1"
    S_NIK = "2"
    S_NET = "3"
    S_WHERE = "4"
