# Use an official NVIDIA CUDA image with Python
FROM ubuntu:20.04

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
    python3 \
    python3-pip \
    tesseract-ocr \
    libcurl4-openssl-dev \
    libssl-dev \
    build-essential \
    libopencv-dev \
    libgl1-mesa-glx \          # Install OpenGL library (libGL.so.1)
    libglib2.0-0 \             # Install glib (required by OpenCV)
    libx11-dev \               # Install X11 (required for GUI-based apps)
    && rm -rf /var/lib/apt/lists/*
# Copy project files into container
COPY . /app

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Set the PYTHONPATH (optional, but helps with imports)
ENV PYTHONPATH=/app

# Run the script using the module path
CMD ["python3", "-m", "project.app"]