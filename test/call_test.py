from io import BytesIO
from pathlib import Path

import requests
from PIL import Image

if __name__ == "__main__":
    api_url = "http://localhost:8067/ocr"

    img = Image.open(Path(__file__).parent.parent / "images" / "img.png")

    image_bytes = BytesIO()
    img.save(image_bytes, format="PNG")
    image_bytes.seek(0)

    response = requests.post(api_url, files={"image": ("img.png", image_bytes, "image/png")})
    print(response.json())
