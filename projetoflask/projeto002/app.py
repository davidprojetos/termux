from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_sqlalchemy import SQLAlchemy
import yt_dlp
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///audios.db'
db = SQLAlchemy(app)

class Audio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250))
    url = db.Column(db.String(500))
    file_path = db.Column(db.String(500))

@app.route('/')
def index():
    audios = Audio.query.all()
    return render_template('index.html', audios=audios)

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        original_file_path = os.path.join('downloads', info_dict['title'] + '.' + info_dict['ext'])
        if os.path.exists(original_file_path):
            file_name = info_dict['title'] + '.mp3'
            file_path = os.path.join('downloads', file_name)
            os.rename(original_file_path, file_path)
            audio = Audio(title=info_dict['title'], url=url, file_path=file_path)
            db.session.add(audio)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return "Erro: O arquivo original não foi encontrado."

@app.route('/play/<audio_id>')
def play(audio_id):
    audio = Audio.query.get(audio_id)
    return send_file(audio.file_path)

@app.route('/edit/<int:audio_id>', methods=['POST'])
def edit_audio(audio_id):
    audio = Audio.query.get(audio_id)
    new_title = request.form['new_title']
    audio.title = new_title
    db.session.commit()
    return redirect(url_for('index'))
    
@app.route('/limpar-tabela', methods=['POST'])
def limpar_tabela():
    try:
        # Exclui todos os registros da tabela Audio
        db.session.query(Audio).delete()
        db.session.commit()
        return redirect(url_for('index'))
    except Exception as e:
        db.session.rollback()
        return "Erro ao limpar a tabela: " + str(e)

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


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
