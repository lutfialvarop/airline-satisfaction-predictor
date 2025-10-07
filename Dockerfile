# Dockerfile

# base image Python
FROM python:3.9-slim

# Instal Supervisor dari package manager sistem
RUN apt-get update && apt-get install -y supervisor

# Tetapkan direktori kerja
WORKDIR /app

# Salin file requirements
COPY requirements.txt .

# Instal semua library Python
RUN pip install --no-cache-dir -r requirements.txt

# Salin file konfigurasi Supervisor ke lokasinya
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Salin semua file proyek (termasuk app.py, train.py, model.joblib, dll.)
COPY . .

# Buka port untuk Streamlit (8501) dan MLflow (8085)
EXPOSE 8501
EXPOSE 8085

# Perintah utama untuk menjalankan Supervisor
# Supervisor kemudian akan menjalankan MLflow dan Streamlit sesuai konfigurasi
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf"]