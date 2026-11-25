"""Проверка синтаксически корректных e-mail адресов.

Модуль содержит регулярное выражение для валидации e-mail.
"""

import re

# Шаблон для полной проверки одного адреса.
FULL_EMAIL_PATTERN = re.compile(
    r"[A-Za-z0-9](?:[A-Za-z0-9._%+-]*[A-Za-z0-9_%+-])?"
    r"@"
    r"(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?\.)+"
    r"[A-Za-z]{2,}"
)

MAX_LOCAL_LENGTH = 64   # максимальная длина локальной части по RFC 5321
MAX_EMAIL_LENGTH = 254  # максимальная длина всего адреса по RFC 5321


def is_valid_email(email):
    """Проверяет, является ли строка синтаксически корректным e-mail."""
    if not isinstance(email, str) or not email:
        return False
    if len(email) > MAX_EMAIL_LENGTH:
        return False
    match = FULL_EMAIL_PATTERN.fullmatch(email)
    if match is None:
        return False
    local_part = email.split("@")[0]
    if len(local_part) > MAX_LOCAL_LENGTH:
        return False
    # локальная часть не должна содержать две точки подряд
    if ".." in local_part:
        return False
    return True


# Регулярное выражение для поиска e-mail в тексте.
EMAIL_PATTERN = re.compile(
    r"(?<![\w.+-])"                   # слева не должно быть части адреса
    r"[A-Za-z0-9](?:[A-Za-z0-9._%+-]*[A-Za-z0-9_%+-])?"
    r"@"
    r"(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?\.)+"
    r"[A-Za-z]{2,}"                    # домен верхнего уровня
    r"(?![\w-])"                      # справа не должно быть части адреса
)


def find_emails(text):
    """Ищет все синтаксически корректные e-mail в тексте.

    Возвращает список уникальных адресов в порядке появления.
    """
    found = EMAIL_PATTERN.findall(text)
    valid = [addr for addr in found if is_valid_email(addr)]
    # убираем дубликаты, сохраняя порядок
    return list(dict.fromkeys(valid))
