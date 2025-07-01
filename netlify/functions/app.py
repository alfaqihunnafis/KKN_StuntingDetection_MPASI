# netlify/functions/app.py

import sys
from pathlib import Path

# Menambahkan direktori root proyek ke path agar bisa mengimpor 'app' dari file utama
sys.path.append(str(Path(__file__).resolve().parents[2]))

from app import app as flask_app # Mengimpor instance Flask dari file app.py utama Anda
from serverless_wsgi import handle

def handler(event, context):
    """
    Fungsi handler yang akan dipanggil oleh Netlify.
    Meneruskan event ke aplikasi Flask menggunakan serverless-wsgi.
    """
    return handle(flask_app, event, context)
