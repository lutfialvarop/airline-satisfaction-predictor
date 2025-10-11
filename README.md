
# 🛫 Airline Satisfaction App

Aplikasi **Airline Passenger Satisfaction** berbasis **Machine Learning (Random Forest Classifier)** untuk memprediksi tingkat kepuasan penumpang berdasarkan data penerbangan.  
Aplikasi ini dikemas dalam **Docker container**, dan bisa **auto-update** menggunakan **Watchtower** agar selalu memakai versi terbaru dari Docker Hub.

---

## 🚀 Fitur Utama
- Prediksi tingkat kepuasan (`satisfied` / `neutral or dissatisfied`)
- Pipeline ML lengkap (training, tuning, evaluasi, MLflow)
- CI/CD otomatis via **GitHub Actions**
- Auto-update container lokal dengan **Watchtower**

---

## 🐳 Docker Deployment Guide

### 1️⃣ Pull Image dari Docker Hub
```bash
docker pull <username>/airline-satisfaction-app:latest
```
---
### 2️⃣ Jalankan Container

```bash
docker run -d -p 8501:8501 -p 8085:8085 --name airline-container <username>/airline-satisfaction-app
```

Penjelasan:

* `-d` → jalankan di background
* `-p 8501:8501` → port default Streamlit
* `-p 8085:8085` → port tambahan (API / service lain)
* `--name airline-container` → nama container
* `<username>/airline-satisfaction-app` → nama image

Buka aplikasi di browser:
* 👉 Streamlit: [http://localhost:8501](http://localhost:8501)
* 👉 MLflow: [http://localhost:8085](http://localhost:8085)

---

## 🔄 3️⃣ Menambahkan Watchtower (Auto-Update Lokal)

Watchtower akan memantau container kamu dan otomatis *pull image terbaru* dari Docker Hub jika ada update baru.

### 🧰 Jalankan Watchtower

```bash
docker run -d \
  --name watchtower \
  -v /var/run/docker.sock:/var/run/docker.sock \
  containrrr/watchtower \
  airline-container \
  --interval 60
```

Penjelasan:

* `-v /var/run/docker.sock:/var/run/docker.sock` → memberi Watchtower akses ke Docker Engine lokal
* `airline-container` → nama container yang ingin dipantau
* `--interval 60` → cek update setiap 60 detik
* ⚠️ **Gunakan ini hanya di lokal**, jangan di server production (karena bisa update saat model sedang berjalan).

Untuk menghentikan Watchtower:

```bash
docker stop watchtower && docker rm watchtower
```
---

## 🧰 Troubleshooting

| Masalah                          | Solusi                                               |
| -------------------------------- | ---------------------------------------------------- |
| Port 8501 sudah digunakan        | Jalankan di port lain: `-p 8600:8501`                |
| Container tidak update otomatis  | Pastikan Watchtower sedang berjalan                  |
