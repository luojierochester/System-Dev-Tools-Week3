"""Regression tests for the greeting CLI."""

import sys

import pytest

from greetlab.cli import main


def test_valid_name_is_trimmed(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["sdt-greet", "--name", "  Luo  "])
    main()
    assert capsys.readouterr().out == "Hello, Luo!\n"


def test_blank_name_exits_with_status_2(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["sdt-greet", "--name", "   "])
    with pytest.raises(SystemExit) as error:
        main()
    assert error.value.code == 2
    assert "name must not be blank" in capsys.readouterr().err
