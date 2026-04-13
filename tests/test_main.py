import json
import os
from unittest.mock import patch

from main import escape_string, load_published_ids, save_published_ids


class TestEscapeString:
    def test_escapes_underscore(self):
        assert escape_string("hello_world") == r"hello\_world"

    def test_escapes_asterisk(self):
        assert escape_string("bold*text") == r"bold\*text"

    def test_escapes_square_brackets(self):
        assert escape_string("[link]") == r"\[link\]"

    def test_escapes_parentheses(self):
        assert escape_string("(text)") == r"\(text\)"

    def test_escapes_tilde(self):
        assert escape_string("~strike~") == r"\~strike\~"

    def test_escapes_dot(self):
        assert escape_string("end.") == r"end\."

    def test_escapes_exclamation(self):
        assert escape_string("hello!") == r"hello\!"

    def test_plain_text_unchanged(self):
        assert escape_string("Hello World") == "Hello World"

    def test_empty_string(self):
        assert escape_string("") == ""

    def test_multiple_specials(self):
        result = escape_string("a_b*c")
        assert result == r"a\_b\*c"


class TestLoadPublishedIds:
    def test_returns_list_from_env(self):
        ids = [1, 2, 3]
        with patch.dict(os.environ, {"PUBLISHED_IDS": json.dumps(ids)}):
            result = load_published_ids()
        assert result == ids

    def test_returns_empty_list_when_env_missing(self):
        env = {k: v for k, v in os.environ.items() if k != "PUBLISHED_IDS"}
        with patch.dict(os.environ, env, clear=True):
            result = load_published_ids()
        assert result == []

    def test_returns_empty_list_on_invalid_json(self):
        with patch.dict(os.environ, {"PUBLISHED_IDS": "not-json"}):
            result = load_published_ids()
        assert result == []


class TestSavePublishedIds:
    def test_calls_update_github_variable(self):
        ids = [10, 20, 30]
        with patch("main.update_github_variable") as mock_update:
            save_published_ids(ids)
        mock_update.assert_called_once_with("PUBLISHED_IDS", json.dumps(ids))

    def test_saves_empty_list(self):
        with patch("main.update_github_variable") as mock_update:
            save_published_ids([])
        mock_update.assert_called_once_with("PUBLISHED_IDS", "[]")
