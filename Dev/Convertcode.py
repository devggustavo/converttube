import os
from flask import Flask, render_template, request
from pytube import YouTube
import validators
from datetime import datetime, timedelta

app = Flask(__name__)

# Dicionário para armazenar os links e o momento do último download
links_utilizados = {}

def is_valid_youtube_url(url):
    return validators.url(url) and ('youtube.com' in url or 'youtu.be' in url)

def executar_download(link):
    try:
        if not is_valid_youtube_url(link):
            return "invalid_link"

        # Verifica se o link foi utilizado recentemente para download
        if link in links_utilizados and datetime.now() - links_utilizados[link] < timedelta(hours=1):
            return "recent_download"

        video = YouTube(link)
        audio_stream = video.streams.filter(only_audio=True, file_extension="mp4").first()

        download_path = os.path.join(os.path.expanduser("~"), "Downloads")
        musicas_path = os.path.join(download_path, "Musicas mp3")
        os.makedirs(musicas_path, exist_ok=True)

        audio_stream.download(output_path=musicas_path)

        # Atualiza o momento do último download para o link
        links_utilizados[link] = datetime.now()

        return "success"

    except Exception as e:
        return "error"

@app.route('/')
def index():
    return render_template('indexConvert.html')

@app.route('/download', methods=['POST'])
def download():
    link = request.form['link']
    status = executar_download(link)
    return render_template('indexConvert.html', status=status)

if __name__ == '__main__':
    app.run(debug=True)

