"""Unit-тесты для модуля email_validator."""

import os
import tempfile
import unittest

from email_validator import (
    find_emails,
    find_emails_in_file,
    find_emails_on_webpage,
    is_valid_email,
)


class TestIsValidEmail(unittest.TestCase):
    """Тесты проверки корректности одного e-mail адреса."""

    def test_simple_valid_email(self):
        self.assertTrue(is_valid_email("user@example.com"))

    def test_valid_email_with_digits_and_dots(self):
        self.assertTrue(is_valid_email("ivan.petrov123@mail.ru"))

    def test_valid_email_with_plus_and_percent(self):
        self.assertTrue(is_valid_email("user+tag%d@example.org"))

    def test_valid_email_with_subdomain(self):
        self.assertTrue(is_valid_email("admin@mail.corp.example.co.uk"))

    def test_valid_email_with_hyphen_in_domain(self):
        self.assertTrue(is_valid_email("info@my-company-site.net"))

    def test_valid_long_tld(self):
        self.assertTrue(is_valid_email("user@example.museum"))

    def test_empty_string(self):
        self.assertFalse(is_valid_email(""))

    def test_none_value(self):
        self.assertFalse(is_valid_email(None))

    def test_no_at_sign(self):
        self.assertFalse(is_valid_email("userexample.com"))

    def test_no_local_part(self):
        self.assertFalse(is_valid_email("@example.com"))

    def test_no_domain(self):
        self.assertFalse(is_valid_email("user@"))

    def test_no_tld(self):
        self.assertFalse(is_valid_email("user@example"))

    def test_tld_too_short(self):
        self.assertFalse(is_valid_email("user@example.c"))

    def test_tld_with_digits(self):
        self.assertFalse(is_valid_email("user@example.c0m"))

    def test_double_at_sign(self):
        self.assertFalse(is_valid_email("user@@example.com"))

    def test_space_in_email(self):
        self.assertFalse(is_valid_email("us er@example.com"))

    def test_local_part_starts_with_dot(self):
        self.assertFalse(is_valid_email(".user@example.com"))

    def test_local_part_ends_with_dot(self):
        self.assertFalse(is_valid_email("user.@example.com"))

    def test_double_dot_in_local_part(self):
        self.assertFalse(is_valid_email("us..er@example.com"))

    def test_domain_label_starts_with_hyphen(self):
        self.assertFalse(is_valid_email("user@-example.com"))

    def test_domain_label_ends_with_hyphen(self):
        self.assertFalse(is_valid_email("user@example-.com"))

    def test_local_part_too_long(self):
        local_part = "a" * 65
        self.assertFalse(is_valid_email(f"{local_part}@example.com"))

    def test_email_too_long(self):
        local_part = "a" * 64
        domain = "b" * 200 + ".com"
        self.assertFalse(is_valid_email(f"{local_part}@{domain}"))


class TestFindEmails(unittest.TestCase):
    """Тесты поиска e-mail в тексте."""

    def test_find_single_email(self):
        text = "Напишите мне на ivan@example.com, пожалуйста."
        self.assertEqual(find_emails(text), ["ivan@example.com"])

    def test_find_multiple_emails(self):
        text = "Контакты: a@b.ru и sales@shop-online.com."
        self.assertEqual(
            find_emails(text), ["a@b.ru", "sales@shop-online.com"]
        )

    def test_no_duplicates_in_result(self):
        text = "a@b.ru, a@b.ru, c@d.ru"
        self.assertEqual(find_emails(text), ["a@b.ru", "c@d.ru"])

    def test_invalid_candidates_are_skipped(self):
        text = "Почта: bad@mail и good@mail.ru"
        self.assertEqual(find_emails(text), ["good@mail.ru"])

    def test_trailing_punctuation_is_not_included(self):
        text = "Напишите на user@example.com."
        self.assertEqual(find_emails(text), ["user@example.com"])

    def test_exclamation_after_email(self):
        text = "Почта admin@site.ru!"
        self.assertEqual(find_emails(text), ["admin@site.ru"])

    def test_empty_text(self):
        self.assertEqual(find_emails(""), [])

    def test_text_without_emails(self):
        self.assertEqual(find_emails("Здесь нет почтовых адресов."), [])


class TestFindEmailsInFile(unittest.TestCase):
    """Тесты поиска e-mail в файле."""

    def test_find_in_existing_file(self):
        with tempfile.NamedTemporaryFile(
            "w", suffix=".txt", encoding="utf-8", delete=False
        ) as tmp:
            tmp.write("Пишите: support@site.ru или admin@site.ru")
            tmp_path = tmp.name
        try:
            self.assertEqual(
                find_emails_in_file(tmp_path),
                ["support@site.ru", "admin@site.ru"],
            )
        finally:
            os.unlink(tmp_path)

    def test_missing_file_raises_error(self):
        with self.assertRaises(FileNotFoundError):
            find_emails_in_file("no_such_file_12345.txt")


class TestFindEmailsOnWebpage(unittest.TestCase):
    """Тесты проверки URL при поиске на веб-странице."""

    def test_invalid_scheme_raises_value_error(self):
        with self.assertRaises(ValueError):
            find_emails_on_webpage("ftp://example.com")

    def test_plain_text_raises_value_error(self):
        with self.assertRaises(ValueError):
            find_emails_on_webpage("example.com")


if __name__ == "__main__":
    unittest.main()
