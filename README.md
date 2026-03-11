# OCR Microservice

A RESTful microservice for Optical Character Recognition (OCR) built with FastAPI and PaddleOCR. Upload an image and get back the extracted text.

## Features

- Text extraction from images (PNG, JPG, etc.)
- Angle detection for rotated text
- Multi-language support (default: English)
- Docker support

## Requirements

- Python 3.8+
- pip

## Dependencies

### Production (`requirements.txt`)

| Package | Purpose |
|---|---|
| `paddlepaddle` | PaddleOCR inference engine |
| `paddleocr` | OCR implementation |
| `fastapi` | Web framework |
| `uvicorn` | ASGI server |
| `opencv-python` | Image processing |
| `python-multipart` | Multipart file upload handling |
| `Pillow` | Image I/O |

### Development (`requirements-dev.txt`)

Includes all production dependencies, plus:

| Package | Purpose |
|---|---|
| `pytest` | Test runner |
| `httpx` | HTTP client used by FastAPI `TestClient` |
| `requests` | HTTP client for manual test scripts |
| `pyperclip` | Clipboard integration (`ocr_app.py`) |

## Installation

**Production:**

```bash
pip install -r requirements.txt
```

**Development:**

```bash
pip install -r requirements-dev.txt
```

## Running

### Locally

```bash
python -m project.app
```

The service will be available at `http://localhost:8067`.

### With Docker

```bash
docker build -t ocr-microservice .
docker run -p 8067:8067 ocr-microservice
```

### With Docker Compose

```bash
docker-compose up
```

## API

### `POST /ocr`

Extract text from an uploaded image.

**Request**

| Parameter | Type       | Required | Description        |
|-----------|------------|----------|--------------------|
| `image`   | UploadFile | Yes      | Image file to process |

**Example**

```bash
curl -X POST "http://localhost:8067/ocr" \
  -F "image=@path/to/image.png"
```

**Response**

```json
"extracted text from the image"
```

## Project Structure

```
OCR_Microservice/
├── project/
│   ├── app.py              # FastAPI application entry point
│   ├── classes/
│   │   └── OCR.py          # PaddleOCR wrapper
│   └── routes/
│       └── routes.py       # API route definitions
├── test/
│   ├── test_api.py         # API endpoint tests (pytest)
│   ├── test_ocr.py         # OCR class unit tests (pytest)
│   ├── call_test.py        # Manual integration script
│   └── ocr_app.py          # Windows clipboard integration script
├── images/
│   └── img.png             # Sample test image
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── requirements-dev.txt
```

## Testing

Run the full test suite with pytest:

```bash
pytest test/
```

For a manual integration check against a running service:

```bash
python test/call_test.py
```

For the Windows clipboard workflow (copies image from clipboard, sends to API, copies result back):

```bash
python test/ocr_app.py
```
