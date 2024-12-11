# Tahap 1: Build stage untuk menginstal dependencies
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt
COPY . .
EXPOSE 5000

# Menjalankan aplikasi Flask
CMD ["python","app.py"]
