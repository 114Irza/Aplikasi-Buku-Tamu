import os
import time
from flask import Flask, render_template, request, redirect, url_for, jsonify
import pymysql

app = Flask(__name__)

# Konfigurasi database dari environment variables
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'root')
DB_NAME = os.environ.get('DB_NAME', 'guestbook')
DB_PORT = int(os.environ.get('DB_PORT', 3306))


def get_db_connection():
    """Membuat koneksi ke database MySQL."""
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )


def init_db():
    """Inisialisasi database dan tabel jika belum ada."""
    # Tunggu MySQL siap (penting saat menggunakan docker-compose)
    retries = 10
    while retries > 0:
        try:
            conn = pymysql.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                port=DB_PORT,
                charset='utf8mb4'
            )
            # Buat database jika belum ada
            with conn.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`")
            conn.close()

            # Buat tabel di database
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS messages (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100) NOT NULL,
                        message TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                ''')
            conn.commit()
            conn.close()
            print("Database berhasil diinisialisasi!")
            return
        except pymysql.err.OperationalError:
            retries -= 1
            print(f"Menunggu MySQL siap... (sisa percobaan: {retries})")
            time.sleep(3)

    print("GAGAL: Tidak dapat terhubung ke MySQL.")


@app.route('/', methods=['GET', 'POST'])
def index():
    """Halaman utama: form input dan daftar pesan."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        message = request.form.get('message', '').strip()

        if name and message:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute(
                    'INSERT INTO messages (name, message) VALUES (%s, %s)',
                    (name, message)
                )
            conn.commit()
            conn.close()

        return redirect(url_for('index'))

    # Ambil semua pesan dari database
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM messages ORDER BY created_at DESC')
        messages = cursor.fetchall()
    conn.close()

    return render_template('index.html', messages=messages)


@app.route('/health')
def health():
    """Health check endpoint untuk monitoring."""
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute('SELECT 1')
        conn.close()
        return jsonify({'status': 'healthy', 'database': 'connected'}), 200
    except Exception as e:
        return jsonify({'status': 'unhealthy', 'error': str(e)}), 500


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)
