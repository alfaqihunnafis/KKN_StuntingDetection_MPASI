# Gunakan image Python resmi sebagai dasar
FROM python:3.9-slim

# Tetapkan direktori kerja di dalam container
WORKDIR /app

# Salin file requirements.txt terlebih dahulu untuk caching layer
COPY requirements.txt .

# Instal dependensi yang dibutuhkan
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file proyek ke dalam direktori kerja
COPY . .

# Perintah untuk menjalankan aplikasi Flask dengan Gunicorn (server produksi)
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:$PORT", "app:app"]
