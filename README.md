# 📖 Buku Tamu (Guestbook)

Aplikasi web Buku Tamu sederhana yang dibangun menggunakan **Python Flask** dan **MySQL**, dikontainerisasi dengan **Docker**.

## 📁 Struktur Proyek

```
Buku_Tamu/
├── source-code/
│   ├── app.py              # Aplikasi Flask utama
│   ├── requirements.txt    # Dependency Python
│   └── templates/
│       └── index.html      # Halaman web (form + daftar pesan)
├── tests/
│   └── test_app.py         # Automated test (pytest)
├── Dockerfile              # Konfigurasi Docker image
├── docker-compose.yml      # Multi-service (app + MySQL)
├── README.md               # Dokumentasi proyek
└── .github/
    └── workflows/
        └── ci.yml          # Pipeline CI/CD GitHub Actions
```

## 🚀 Cara Menjalankan

### Prasyarat

- [Docker](https://docs.docker.com/get-docker/) dan [Docker Compose](https://docs.docker.com/compose/install/) sudah terinstall.

### Menjalankan dengan Docker Compose

```bash
# Clone repository
git clone https://github.com/username/Buku_Tamu.git
cd Buku_Tamu

# Jalankan semua service
docker-compose up --build

# Atau jalankan di background
docker-compose up --build -d
```

Akses aplikasi di browser: **http://localhost:5000**

### Menghentikan Aplikasi

```bash
docker-compose down

# Untuk menghapus volume data juga:
docker-compose down -v
```

## 🧪 Menjalankan Test

```bash
# Install dependency
pip install -r source-code/requirements.txt

# Jalankan test
pytest tests/ -v
```

## ⚙️ CI/CD Pipeline

Pipeline GitHub Actions otomatis berjalan saat:
- **Push** ke branch `main`
- **Pull Request** ke branch `main`

Tahapan pipeline:
1. ✅ Checkout source code
2. ✅ Setup Python 3.11
3. ✅ Install dependencies
4. ✅ Run automated tests (pytest)
5. ✅ Build Docker image

## 🛠️ Teknologi

| Komponen   | Teknologi      |
|------------|----------------|
| Backend    | Python + Flask |
| Database   | MySQL 8.0      |
| Container  | Docker         |
| Orkestrasi | Docker Compose |
| CI/CD      | GitHub Actions |
| Testing    | pytest         |
