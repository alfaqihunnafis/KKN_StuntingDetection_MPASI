from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd

app = Flask(__name__)

# Muat model pengklasifikasi stunting
filename = 'model/modelRF.pkl'
model = pickle.load(open(filename, 'rb'))

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
    if request.method == 'POST':
        file = request.files['file']
        if not file:
            return render_template('kelompok.html', hasil_deteksi=['Tidak ada file yang diupload'])

        try:
            data = pd.read_csv(file, sep=',')
            
            # Kolom di file CSV
            expected_columns = ['Jenis Kelamin','Umur (bulan)','Berat Bayi (kg)','Panjang Bayi (cm)','Berat Badan (kg)','Tinggi Badan (cm)']
            
            # Pastikan semua kolom ada
            if not all(col in data.columns for col in expected_columns):
                return render_template('kelompok.html', hasil_deteksi=['CSV harus mengikuti format: Jenis Kelamin, Umur (bulan), Berat Bayi (kg), Panjang Bayi (cm), Berat Badan (kg), Tinggi Badan (cm)'])

            # Pilih hanya kolom yang dibutuhkan
            data = data[expected_columns]
            
            # Lakukan deteksi
            predictions = model.predict(data)
            results = ['Anak Mengalami Stunting' if pred == 1 else 'Anak Tidak Mengalami Stunting' for pred in predictions]

            return render_template('kelompok.html', hasil_deteksi=results)

        except Exception as e:
            return render_template('kelompok.html', hasil_deteksi=[f'Error processing file: {str(e)}'])

if __name__ == '__main__':
    app.run(debug=True)