"""Проверка и поиск синтаксически корректных e-mail адресов.

Модуль содержит регулярное выражение для валидации e-mail и функции
поиска адресов в тексте, файле и на веб-странице.
"""

import re
import urllib.request

# Регулярное выражение для поиска e-mail в тексте.
# Локальная часть: буквы, цифры и символы ._%+- (не начинается/не оканчивается точкой).
# Домен: метки из букв, цифр и дефисов, разделённые точками.
# TLD: минимум 2 буквы.
EMAIL_PATTERN = re.compile(
    r"(?<![\w.+-])"                    # слева не должно быть части адреса
    r"[A-Za-z0-9](?:[A-Za-z0-9._%+-]*[A-Za-z0-9_%+-])?"  # локальная часть
    r"@"
    r"(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?\.)+"   # доменные метки
    r"[A-Za-z]{2,}"                    # домен верхнего уровня
    r"(?![\w-])"                       # справа не должно быть части адреса
)

# Шаблон для полной проверки одного адреса (без границ поиска).
FULL_EMAIL_PATTERN = re.compile(
    r"[A-Za-z0-9](?:[A-Za-z0-9._%+-]*[A-Za-z0-9_%+-])?"
    r"@"
    r"(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?\.)+"
    r"[A-Za-z]{2,}"
)

MAX_LOCAL_LENGTH = 64   # максимальная длина локальной части по RFC 5321
MAX_EMAIL_LENGTH = 254  # максимальная длина всего адреса по RFC 5321

REQUEST_TIMEOUT = 10  # таймаут загрузки веб-страницы в секундах


def is_valid_email(email):
    """Проверяет, является ли строка синтаксически корректным e-mail.

    Args:
        email: проверяемая строка.

    Returns:
        True, если строка — корректный e-mail, иначе False.
    """
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


def find_emails(text):
    """Ищет все синтаксически корректные e-mail в тексте.

    Args:
        text: текст для поиска.

    Returns:
        Список найденных уникальных e-mail в порядке появления.
    """
    found = EMAIL_PATTERN.findall(text)
    # отбрасываем кандидатов, не проходящих полную проверку
    valid = [addr for addr in found if is_valid_email(addr)]
    # убираем дубликаты, сохраняя порядок
    return list(dict.fromkeys(valid))


def find_emails_in_file(file_path, encoding="utf-8"):
    """Ищет e-mail адреса в текстовом файле.

    Args:
        file_path: путь к файлу.
        encoding: кодировка файла (по умолчанию utf-8).

    Returns:
        Список найденных уникальных e-mail.

    Raises:
        FileNotFoundError: если файл не существует.
    """
    with open(file_path, "r", encoding=encoding) as file:
        text = file.read()
    return find_emails(text)


def find_emails_on_webpage(url):
    """Ищет e-mail адреса на веб-странице по URL.

    Args:
        url: адрес веб-страницы (http:// или https://).

    Returns:
        Список найденных уникальных e-mail.

    Raises:
        ValueError: если URL имеет недопустимую схему.
        urllib.error.URLError: если страницу не удалось загрузить.
    """
    if not url.startswith(("http://", "https://")):
        raise ValueError("URL должен начинаться с http:// или https://")
    request = urllib.request.Request(
        url, headers={"User-Agent": "Mozilla/5.0 (email-regex-lab)"}
    )
    with urllib.request.urlopen(request, timeout=REQUEST_TIMEOUT) as response:
        html = response.read().decode("utf-8", errors="ignore")
    return find_emails(html)
