from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
import os
import yt_dlp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///audios.db'
db = SQLAlchemy(app)

class Audio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    url = db.Column(db.String(500))
    file_name = db.Column(db.String(500))

@app.route('/')
def index():
    audios = Audio.query.all()
    return render_template('index.html', audios=audios)

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        id = info_dict['id']
        title = info_dict['title']
        audio = Audio(title=title, url=url, file_name=id)
        db.session.add(audio)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/play/<int:audio_id>')
def play(audio_id):
    audio = Audio.query.get(audio_id)
    file_path = os.path.join('downloads', f"{audio.file_name}.mp3")
    return send_file(file_path)

@app.route('/limpar-downloads', methods=['POST'])
def limpar_downloads():
    folder = 'downloads'
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Erro ao excluir o arquivo {file_path}: {e}")
    return redirect(url_for('index'))

@app.route('/limpar-tabela', methods=['POST'])
def limpar_tabela():
    try:
        Audio.query.delete()
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        return f"Erro ao limpar a tabela: {str(e)}"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


