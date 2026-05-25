# 1. Start with a lightweight Linux/Python computer
FROM python:3.10-slim

# 2. Install Tesseract-OCR and Poppler (needed for pdf2image)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# 3. Set the working directory inside the cloud computer
WORKDIR /app

# 4. Copy your requirements and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Download the Spacy English AI model
RUN python -m spacy download en_core_web_sm

# 6. Copy all your actual code (app.py, json files, etc.) into the cloud
COPY . .

# 7. Start the server using Gunicorn!
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "--timeout", "120", "app:app"]