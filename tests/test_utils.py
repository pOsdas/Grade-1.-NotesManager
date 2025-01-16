from datetime import datetime
import pytest

from utils.date_validator import format_date


def test_format_date_valid():
    # Проверяем корректный формат
    result = format_date("2025/12/14")
    assert result == datetime(2025, 12, 14, 0, 0)


def test_format_date_invalid():
    # Проверяем некорректный формат
    result = "2025^^12^^14"
    with pytest.raises(ValueError) as exc_info:
        format_date(result)

    assert str(exc_info.value) == "Формат даты не поддерживается: 2025^^12^^14"

