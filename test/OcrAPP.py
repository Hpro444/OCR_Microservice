import pyperclip
import requests
from PIL import ImageGrab
from io import BytesIO


def send_image_to_api(image_bytes, api_url):
    """
    Sends an image to the OCR API for processing.

    :param image_bytes: The image bytes to be sent.
    :param api_url: The URL of the OCR API.
    :return: The response from the API.
    """
    response = requests.post(api_url, files={"image": ("clipboard_image.png", image_bytes, "image/png")})
    return response.json()


def get_image_from_clipboard():
    """
    Retrieves an image from the clipboard (Windows only).

    :return: The image as bytes or None if no image is found.
    """
    try:
        # Try to retrieve the image from the clipboard
        img = ImageGrab.grabclipboard()  # This grabs the image from clipboard
        if img:
            # Save the image to a byte buffer
            image_bytes = BytesIO()
            img.save(image_bytes, format="PNG")  # Save it as PNG to keep the format consistent
            image_bytes.seek(0)  # Reset the buffer position
            return image_bytes
        else:
            print("No image found in clipboard.")
            return None
    except Exception as e:
        print(f"Error retrieving image from clipboard: {e}")
        return None


def copy_text_to_clipboard(text):
    """
    Copies the provided text to the clipboard.

    :param text: The text to be copied to the clipboard.
    """
    pyperclip.copy(text)
    print("Text copied to clipboard.")

def send_to_ocr():
    # Set the API URL
    api_url = "http://localhost:8067/ocr"

    # Get image from the clipboard
    image_bytes = get_image_from_clipboard()

    if image_bytes:
        # Send the image to the API if an image was found
        response = send_image_to_api(image_bytes, api_url)
        copy_text_to_clipboard(response)
    else:
        print("No image found in clipboard.")

