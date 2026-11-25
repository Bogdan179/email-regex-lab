"""Консольное приложение для проверки и поиска e-mail адресов.

Режимы работы:
    1 — проверка одного адреса, введённого пользователем;
    2 — поиск e-mail в произвольном тексте;
    3 — поиск e-mail в загруженном файле;
    4 — поиск e-mail на веб-странице по URL.
"""

from email_validator import (
    find_emails,
    find_emails_in_file,
    find_emails_on_webpage,
    is_valid_email,
)

MENU = (
    "\nВыберите режим работы:\n"
    "  1 — проверить один e-mail\n"
    "  2 — найти e-mail в тексте\n"
    "  3 — найти e-mail в файле\n"
    "  4 — найти e-mail на веб-странице по URL\n"
    "  0 — выход\n"
    "> "
)


def print_found(emails):
    """Выводит список найденных адресов."""
    if not emails:
        print("Корректные e-mail не найдены.")
        return
    print(f"Найдено адресов: {len(emails)}")
    for number, email in enumerate(emails, start=1):
        print(f"  {number}. {email}")


def check_single_email():
    """Режим 1: проверка одного адреса."""
    email = input("Введите e-mail: ").strip()
    if is_valid_email(email):
        print(f"'{email}' — синтаксически корректный e-mail.")
    else:
        print(f"'{email}' — некорректный e-mail.")


def search_in_text():
    """Режим 2: поиск в тексте, введённом пользователем."""
    print("Введите текст (одной строкой):")
    text = input()
    print_found(find_emails(text))


def search_in_file():
    """Режим 3: поиск в файле."""
    path = input("Введите путь к файлу: ").strip()
    try:
        print_found(find_emails_in_file(path))
    except FileNotFoundError:
        print(f"Ошибка: файл '{path}' не найден.")
    except OSError as error:
        print(f"Ошибка чтения файла: {error}")


def search_on_webpage():
    """Режим 4: поиск на веб-странице по URL."""
    url = input("Введите URL: ").strip()
    try:
        print_found(find_emails_on_webpage(url))
    except ValueError as error:
        print(f"Ошибка: {error}")
    except Exception as error:  # сетевая ошибка, таймаут и т.п.
        print(f"Не удалось загрузить страницу: {error}")


def main():
    """Главный цикл программы."""
    actions = {
        "1": check_single_email,
        "2": search_in_text,
        "3": search_in_file,
        "4": search_on_webpage,
    }
    print("Проверка и поиск синтаксически корректных e-mail")
    while True:
        choice = input(MENU).strip()
        if choice == "0":
            print("Выход.")
            break
        action = actions.get(choice)
        if action is None:
            print("Неизвестный режим, попробуйте снова.")
        else:
            action()


if __name__ == "__main__":
    main()
