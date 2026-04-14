import pytest
import fast_text_proc

class TestTokenize:
    def test_simple_sentence(self):
        text = "Hello World"
        result = fast_text_proc.fast_tokenize(text)
        assert result == ["hello", "world"]

    def test_with_punctuation(self):
        text = "Hello, World! How are you?"
        result = fast_text_proc.fast_tokenize(text)
        # Пунктуация должна быть удалена, слова приведены к нижнему регистру
        assert result == ["hello", "world", "how", "are", "you"]

    def test_empty_string(self):
        assert fast_text_proc.fast_tokenize("") == []

    def test_extra_spaces(self):
        text = "   Hello   World   "
        result = fast_text_proc.fast_tokenize(text)
        assert result == ["hello", "world"]

    def test_mixed_content(self):
        text = "Python3.9 is great!"
        result = fast_text_proc.fast_tokenize(text)
        # Цифры внутри слов сохраняются, пунктуация по краям убирается
        assert result == ["python3.9", "is", "great"]


class TestCleanText:
    def test_basic_cleaning(self):
        text = "Hello, World!"
        result = fast_text_proc.clean_text(text)
        assert result == "hello world"

    def test_multiple_spaces(self):
        text = "Hello    World"
        result = fast_text_proc.clean_text(text)
        assert result == "hello world"

    def test_newlines_and_tabs(self):
        text = "Hello\nWorld\tTest"
        result = fast_text_proc.clean_text(text)
        assert result == "hello world test"

    def test_empty_string(self):
        assert fast_text_proc.clean_text("") == ""


class TestCountWords:
    def test_simple_count(self):
        assert fast_text_proc.count_words("One two three") == 3

    def test_with_punctuation(self):
        # Пунктуация не должна считаться за отдельные слова
        assert fast_text_proc.count_words("One, two, three.") == 3

    def test_empty_string(self):
        assert fast_text_proc.count_words("") == 0

    def test_only_spaces(self):
        assert fast_text_proc.count_words("   ") == 0


class TestExtractEmails:
    def test_single_email(self):
        text = "Contact us at support@example.com"
        result = fast_text_proc.extract_emails(text)
        assert result == ["support@example.com"]

    def test_multiple_emails(self):
        text = "Emails: admin@test.org and user@domain.net"
        result = fast_text_proc.extract_emails(text)
        assert len(result) == 2
        assert "admin@test.org" in result
        assert "user@domain.net" in result

    def test_no_emails(self):
        assert fast_text_proc.extract_emails("No emails here") == []

    def test_invalid_email_format(self):
        # Простая проверка, что строка без @ не считается email
        assert fast_text_proc.extract_emails("user@examplecom") == []


class TestBatchProcessing:
    def test_batch_tokenize(self):
        texts = ["Hello World", "Foo Bar"]
        result = fast_text_proc.batch_tokenize(texts)
        assert result == [["hello", "world"], ["foo", "bar"]]

    def test_batch_clean(self):
        texts = ["Hello!", "World?"]
        result = fast_text_proc.batch_clean(texts)
        assert result == ["hello", "world"]

    def test_empty_batch(self):
        assert fast_text_proc.batch_tokenize([]) == []
        assert fast_text_proc.batch_clean([]) == []