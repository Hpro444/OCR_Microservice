from fastapi import APIRouter, File, UploadFile
from project.classes.OCR import OCR
from PIL import Image
import io


# Define a route to perform OCR on an image
router = APIRouter()

@router.post("/ocr")
async def ocr(image: UploadFile = File(...)):
    # Read the image file as bytes
    image_bytes = await image.read()
    # Call the OCR function here
    ocr = OCR()
    return ocr.ocr_text(image_bytes)

