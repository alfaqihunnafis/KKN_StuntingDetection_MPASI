from flask import Flask, render_template, request, send_file, flash
import pickle
import numpy as np
import pandas as pd
from io import BytesIO
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Set secret key untuk sesi dan flash messages

# Muat model pengklasifikasi stunting
filename = 'model/modelRF.pkl'
model = pickle.load(open(filename, 'rb'))

# Variabel global untuk menyimpan hasil prediksi
csv_output = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/individu')
def individu():
    return render_template('individu.html')

@app.route('/kelompok')
def kelompok():
    return render_template('kelompok.html')

@app.route('/deteksi_individu', methods=['POST'])
def deteksi_individu():
    if request.method == 'POST':
        try:
            # Ambil data dari form
            jenis_kelamin = int(request.form['jenis_kelamin'])
            umur = int(request.form['umur'])
            berat_bayi = float(request.form['berat_bayi'])
            panjang_bayi = float(request.form['panjang_bayi'])
            berat_badan = float(request.form['berat_badan'])
            tinggi_badan = float(request.form['tinggi_badan'])
            
            # Buat array numpy
            data = np.array([[jenis_kelamin, umur, berat_bayi, panjang_bayi, berat_badan, tinggi_badan]])
            
            # Lakukan deteksi
            prediction = model.predict(data)
            # Tentukan output berdasarkan deteksi
            if prediction[0] == 1:
                output = 'Anak Mengalami Stunting'
            else:
                output = 'Anak Tidak Mengalami Stunting'
            
            return render_template('individu.html', deteksi_text=f'Hasil: {output}')
        except Exception as e:
            return render_template('individu.html', deteksi_text=f'Error: {str(e)}')
    return render_template('individu.html')

@app.route('/deteksi_csv', methods=['POST'])
def deteksi_csv():
    global csv_output  # Menggunakan variabel global untuk menyimpan output CSV
    
    if request.method == 'POST':
        file = request.files['file']
        if not file:
            flash('Tidak ada file yang diupload!', 'error')
            return render_template('kelompok.html', csv_available=False)

        try:
            data = pd.read_csv(file, sep=',')
            
            # Cek jika file kosong
            if data.empty:
                flash('File CSV kosong. Mohon unggah file yang berisi data.', 'error')
                return render_template('kelompok.html', csv_available=False)

            # Kolom yang diharapkan di file CSV
            expected_columns = ['Jenis Kelamin','Umur (bulan)','Berat Bayi (kg)','Panjang Bayi (cm)','Berat Badan (kg)','Tinggi Badan (cm)']
            
            # Memastikan semua kolom ada
            if not all(col in data.columns for col in expected_columns):
                flash('Format CSV tidak sesuai. Harus mengandung kolom: Jenis Kelamin, Umur (bulan), Berat Bayi (kg), Panjang Bayi (cm), Berat Badan (kg), Tinggi Badan (cm).', 'error')
                return render_template('kelompok.html', csv_available=False)

            # Memilih kolom yang dibutuhkan
            data = data[expected_columns]
            
            # Melakukan deteksi
            predictions = model.predict(data)
            data['Prediksi Stunting'] = ['Anak Mengalami Stunting' if pred == 1 else 'Anak Tidak Mengalami Stunting' for pred in predictions]

            # Menyimpan hasil prediksi ke dalam file CSV di memori
            output = BytesIO()  # Menggunakan BytesIO untuk mode biner
            data.to_csv(output, index=False)
            output.seek(0)  # Mengembalikan posisi file ke awal
            csv_output = output  # Menyimpan hasil CSV ke variabel global

            # Mengembalikan ke halaman dengan tombol unduhan aktif
            return render_template('kelompok.html', csv_available=True)

        except pd.errors.EmptyDataError:
            flash('File CSV kosong atau tidak valid. Mohon unggah file yang benar.', 'error')
            return render_template('kelompok.html', csv_available=False)

        except Exception as e:
            flash(f'Terjadi kesalahan: {str(e)}', 'error')
            return render_template('kelompok.html', csv_available=False)

@app.route('/download_csv')
def download_csv():
    global csv_output  # Menggunakan variabel global csv_output
    
    if csv_output is None:
        return "Tidak ada hasil prediksi untuk diunduh.", 400

    # Mengirim file CSV untuk diunduh
    return send_file(csv_output, mimetype='text/csv', download_name='hasil_prediksi_stunting.csv', as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)