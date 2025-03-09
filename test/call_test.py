import requests
from PIL import Image
from io import BytesIO

# Set the API URL
api_url = "http://localhost:8067/ocr"

# Open an image file (you can replace this with any image file you like)
img = Image.open("../images/img.png")

# Save the image as bytes
image_bytes = BytesIO()
img.save(image_bytes, format="PNG")  # Use PNG format to match the input image
image_bytes.seek(0)  # Reset the buffer position

# Send a POST request to the API
response = requests.post(api_url, files={"image": ("img.png", image_bytes, "image/png")})

# Print the response
print(response.json())
