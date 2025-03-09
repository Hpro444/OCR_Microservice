from paddleocr import PaddleOCR
from PIL import Image
import io


class OCR:
    def __init__(self, lang="en", use_angle_cls=True):
        self.ocr = PaddleOCR(lang=lang, use_angle_cls=use_angle_cls)

    def ocr_text(self, image_bytes: bytes) -> str:

        # Perform OCR on the image
        results = self.ocr.ocr(image_bytes)

        detected_text = ""
        for result in results:
            for line in result:
                text, confidence = line[1]
                detected_text += f"{text} "

        return detected_text