from io import BytesIO
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient
from PIL import Image

from project.app import app

client = TestClient(app)


def make_image_bytes(text_color=(0, 0, 0), bg_color=(255, 255, 255)) -> BytesIO:
    """Create a minimal valid PNG image in memory."""
    img = Image.new("RGB", (100, 50), color=bg_color)
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    return buf


@pytest.fixture(autouse=True)
def mock_ocr():
    """Patch PaddleOCR for all API tests to avoid loading heavy models."""
    with patch("project.classes.ocr.PaddleOCR") as mock_paddle:
        mock_instance = MagicMock()
        mock_paddle.return_value = mock_instance
        mock_instance.ocr.return_value = [
            [[None, ("mocked text", 0.99)]]
        ]
        yield mock_instance


def test_ocr_endpoint_returns_200():
    response = client.post("/ocr", files={"image": ("test.png", make_image_bytes(), "image/png")})
    assert response.status_code == 200


def test_ocr_endpoint_returns_text(mock_ocr):
    mock_ocr.ocr.return_value = [[[None, ("hello world", 0.99)]]]
    response = client.post("/ocr", files={"image": ("test.png", make_image_bytes(), "image/png")})
    assert "hello world" in response.json()


def test_ocr_endpoint_missing_file():
    response = client.post("/ocr")
    assert response.status_code == 422


def test_ocr_endpoint_accepts_jpg():
    buf = BytesIO()
    Image.new("RGB", (100, 50)).save(buf, format="JPEG")
    buf.seek(0)
    response = client.post("/ocr", files={"image": ("test.jpg", buf, "image/jpeg")})
    assert response.status_code == 200


def test_ocr_endpoint_returns_string_type(mock_ocr):
    mock_ocr.ocr.return_value = [[[None, ("sample", 0.9)]]]
    response = client.post("/ocr", files={"image": ("test.png", make_image_bytes(), "image/png")})
    assert isinstance(response.json(), str)


def test_ocr_endpoint_empty_image(mock_ocr):
    mock_ocr.ocr.return_value = [[]]
    response = client.post("/ocr", files={"image": ("empty.png", make_image_bytes(), "image/png")})
    assert response.status_code == 200
    assert response.json() == ""


def test_ocr_endpoint_multiline_text(mock_ocr):
    mock_ocr.ocr.return_value = [
        [
            [None, ("line one", 0.98)],
            [None, ("line two", 0.97)],
        ]
    ]
    response = client.post("/ocr", files={"image": ("test.png", make_image_bytes(), "image/png")})
    result = response.json()
    assert "line one" in result
    assert "line two" in result
