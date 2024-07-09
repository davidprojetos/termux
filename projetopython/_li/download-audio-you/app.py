import os
import random
import string
import yt_dlp
import subprocess
import sqlite3

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('audio_files.db')
c = conn.cursor()

# Criar a tabela se não existir
c.execute('''CREATE TABLE IF NOT EXISTS files
             (original_name text, modified_name text)''')

def generate_random_filename(length=10):
    """Gera um nome de arquivo aleatório com o comprimento especificado."""
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(length))

def download_convert_rename_and_save_to_db(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(title)s.%(ext)s',  # Nome do arquivo de saída
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info_dict)
        
        # Converter para MP3 usando FFmpeg
        mp3_filename = filename[:-4] + '.mp3'
        subprocess.run(['ffmpeg', '-i', filename, '-vn', '-ar', '44100', '-ac', '2', '-ab', '192k', '-f', 'mp3', mp3_filename], check=True)
        
        # Excluir o arquivo WebM após a conversão
        os.remove(filename)
        
        # Renomear o arquivo MP3 com um número aleatório de 10 dígitos
        random_name = generate_random_filename()
        new_filename = f"{random_name}.mp3"
        os.rename(mp3_filename, new_filename)
        
        # Salvar os nomes dos arquivos no banco de dados
        c.execute("INSERT INTO files (original_name, modified_name) VALUES (?, ?)", (info_dict['title'], new_filename))
        conn.commit()
        
        print(f"Arquivo convertido para MP3, arquivo WebM removido e arquivo MP3 renomeado para {new_filename}. Nomes salvos no banco de dados!")

def list_files_from_db():
    """Listar os dados do banco de dados."""
    c.execute("SELECT * FROM files")
    rows = c.fetchall()
    print("Dados do banco de dados:")
    for row in rows:
        print("Nome Original:", row[0])
        print("Nome Modificado:", row[1])
        print("")

# Menu de opções
def main():
    while True:
        print("Selecione uma opção:")
        print("1. Baixar e converter vídeo")
        print("2. Listar arquivos do banco de dados")
        print("3. Sair")
        choice = input("Opção: ")

        if choice == '1':
            video_url = input("Por favor, insira a URL do vídeo do YouTube: ")
            download_convert_rename_and_save_to_db(video_url)
        elif choice == '2':
            list_files_from_db()
        elif choice == '3':
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()

# Fechar a conexão com o banco de dados
conn.close()
