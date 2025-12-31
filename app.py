import os
from flask import Flask, render_template, request, send_file, after_this_request
import yt_dlp

app = Flask(__name__)

# Menggunakan folder /tmp agar aman dari masalah izin akses di Replit
DOWNLOAD_FOLDER = '/tmp/downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    mode = request.form.get('mode')
    
    if not url:
        return "URL YouTube tidak boleh kosong!", 400

    # Pengaturan Download dengan Cookies
    ydl_opts = {
        'cookiefile': 'cookies.txt',  # Membaca file cookie yang kamu buat
        'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        'format': 'bestvideo+bestaudio/best' if mode == 'video' else 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
    }

    if mode == 'audio':
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Ambil informasi video
            info = ydl.extract_info(url, download=True)
            # Dapatkan path file yang baru saja didownload
            file_path = ydl.prepare_filename(info)
            
            # Jika mode audio, nama file akan berubah jadi .mp3
            if mode == 'audio':
                file_path = os.path.splitext(file_path)[0] + '.mp3'

        @after_this_request
        def remove_file(response):
            try:
                # Menghapus file setelah dikirim ke user agar storage tidak penuh
                if os.path.exists(file_path):
                    os.remove(file_path)
            except Exception as error:
                app.logger.error(f"Error menghapus file: {error}")
            return response

        return send_file(file_path, as_attachment=True)

    except Exception as e:
        return f"Terjadi kesalahan: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
    
