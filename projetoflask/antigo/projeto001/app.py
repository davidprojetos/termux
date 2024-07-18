from flask import Flask, render_template, request, redirect, url_for
from pydub import AudioSegment
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if file:
        audio = AudioSegment.from_file(file)
        audio.export('static/audio/uploaded_audio.mp3', format='mp3')
        return redirect(url_for('play'))
    return redirect(request.url)

@app.route('/play')
def play():
    return render_template('play.html', audio_file='uploaded_audio.mp3')

if __name__ == '__main__':
    app.run(debug=True)
