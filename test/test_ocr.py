from unittest.mock import MagicMock, patch

import pytest

from project.classes.ocr import OCR


@pytest.fixture
def ocr_instance():
    with patch("project.classes.ocr.PaddleOCR") as mock_paddle:
        instance = OCR()
        instance.ocr = mock_paddle.return_value
        yield instance


def test_ocr_text_single_line(ocr_instance):
    ocr_instance.ocr.ocr.return_value = [
        [[None, ("Hello World", 0.99)]]
    ]
    result = ocr_instance.ocr_text(b"fake_image_bytes")
    assert "Hello World" in result


def test_ocr_text_multiple_lines(ocr_instance):
    ocr_instance.ocr.ocr.return_value = [
        [
            [None, ("First line", 0.98)],
            [None, ("Second line", 0.97)],
        ]
    ]
    result = ocr_instance.ocr_text(b"fake_image_bytes")
    assert "First line" in result
    assert "Second line" in result


def test_ocr_text_empty_result(ocr_instance):
    ocr_instance.ocr.ocr.return_value = [[]]
    result = ocr_instance.ocr_text(b"fake_image_bytes")
    assert result == ""


def test_ocr_text_returns_string(ocr_instance):
    ocr_instance.ocr.ocr.return_value = [
        [[None, ("Some text", 0.95)]]
    ]
    result = ocr_instance.ocr_text(b"fake_image_bytes")
    assert isinstance(result, str)


def test_ocr_default_language():
    with patch("project.classes.ocr.PaddleOCR") as mock_paddle:
        OCR()
        mock_paddle.assert_called_once_with(lang="en", use_angle_cls=True)


def test_ocr_custom_language():
    with patch("project.classes.ocr.PaddleOCR") as mock_paddle:
        OCR(lang="ch")
        mock_paddle.assert_called_once_with(lang="ch", use_angle_cls=True)


def test_ocr_angle_cls_disabled():
    with patch("project.classes.ocr.PaddleOCR") as mock_paddle:
        OCR(use_angle_cls=False)
        mock_paddle.assert_called_once_with(lang="en", use_angle_cls=False)
