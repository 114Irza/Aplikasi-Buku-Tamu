# Base image Python
FROM python:3.11-slim

# Set working directory di dalam container
WORKDIR /app

# Salin file requirements dan install dependency terlebih dahulu
# (memanfaatkan Docker layer caching)
COPY source-code/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh source code ke dalam container
COPY source-code/ .

# Expose port aplikasi Flask
EXPOSE 5000

# Perintah untuk menjalankan aplikasi
CMD ["python", "app.py"]
