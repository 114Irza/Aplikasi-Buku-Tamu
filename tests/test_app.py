"""
Automated tests untuk aplikasi Buku Tamu.
Menggunakan pytest dan Flask test client.
"""
import sys
import os
import pytest
from unittest.mock import patch, MagicMock

# Tambahkan path source-code agar module app bisa diimport
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'source-code'))

from app import app


@pytest.fixture
def client():
    """Membuat test client Flask."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def mock_db_connection():
    """Helper untuk mock koneksi database."""
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = []
    mock_cursor.__enter__ = MagicMock(return_value=mock_cursor)
    mock_cursor.__exit__ = MagicMock(return_value=False)
    mock_conn.cursor.return_value = mock_cursor
    return mock_conn



class TestBukuTamu:
    """Test suite untuk aplikasi Buku Tamu."""

    @patch('app.get_db_connection')
    def test_halaman_utama_status_200(self, mock_get_db):
        """Test: Halaman utama harus mengembalikan status 200 OK."""
        mock_get_db.return_value = mock_db_connection()

        app.config['TESTING'] = True
        with app.test_client() as client:
            response = client.get('/')
            assert response.status_code == 200

    @patch('app.get_db_connection')
    def test_halaman_utama_berisi_judul(self, mock_get_db):
        """Test: Halaman utama harus mengandung judul 'Buku Tamu'."""
        mock_get_db.return_value = mock_db_connection()

        app.config['TESTING'] = True
        with app.test_client() as client:
            response = client.get('/')
            assert b'Buku Tamu' in response.data

    @patch('app.get_db_connection')
    def test_halaman_utama_berisi_form(self, mock_get_db):
        """Test: Halaman utama harus mengandung form input."""
        mock_get_db.return_value = mock_db_connection()

        app.config['TESTING'] = True
        with app.test_client() as client:
            response = client.get('/')
            assert b'name="name"' in response.data
            assert b'name="message"' in response.data

    @patch('app.get_db_connection')
    def test_health_check(self, mock_get_db):
        """Test: Endpoint /health harus mengembalikan status healthy."""
        mock_conn = mock_db_connection()
        mock_get_db.return_value = mock_conn

        app.config['TESTING'] = True
        with app.test_client() as client:
            response = client.get('/health')
            assert response.status_code == 200
            data = response.get_json()
            assert data['status'] == 'healthy'

    @patch('app.get_db_connection')
    def test_post_pesan_redirect(self, mock_get_db):
        """Test: POST pesan harus redirect ke halaman utama."""
        mock_get_db.return_value = mock_db_connection()

        app.config['TESTING'] = True
        with app.test_client() as client:
            response = client.post('/', data={
                'name': 'Test User',
                'message': 'Pesan test'
            }, follow_redirects=False)
            assert response.status_code == 302
