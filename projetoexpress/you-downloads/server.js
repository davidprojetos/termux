const express = require('express');
const ytdl = require('ytdl-core');
const fs = require('fs');
const path = require('path');

const app = express();
const port = 3000;

app.use(express.urlencoded({ extended: true }));

app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
});

app.post('/download', async (req, res) => {
    const url = req.body.url;

    try {
        const info = await ytdl.getInfo(url);
        const audioFormat = ytdl.filterFormats(info.formats, 'audioonly')[0];

        console.log(`Iniciando o download de: ${info.videoDetails.title}`);

        res.header('Content-Disposition', `attachment; filename="${info.videoDetails.title}.mp3"`);

        const filePath = path.join(__dirname, `${info.videoDetails.title}.mp3`);
        const writeStream = fs.createWriteStream(filePath);

        const videoStream = ytdl(url, { format: audioFormat });

        videoStream.pipe(writeStream);

        // Acompanhando o progresso do download
        videoStream.on('progress', (chunkLength, downloaded, total) => {
            const percentage = (downloaded / total) * 100;
            console.log(`Progresso: ${Math.round(percentage)}%`);
        });

        writeStream.on('finish', () => {
            console.log(`Download concluído para ${info.videoDetails.title}!`);

            res.download(filePath, () => {
                fs.unlinkSync(filePath);
                console.log(`Arquivo removido: ${info.videoDetails.title}.mp3`);
            });
        });

        writeStream.on('error', (err) => {
            console.error('Erro ao gravar o arquivo:', err);
            res.status(500).send('Erro ao fazer o download');
        });

        videoStream.on('error', (err) => {
            console.error('Erro no stream de vídeo:', err);
            res.status(500).send('Erro ao fazer o download');
        });

    } catch (error) {
        console.error('Erro ao obter informações do vídeo:', error);
        res.status(500).send('Erro ao fazer o download');
    }
});

app.listen(port, () => {
    console.log(`Servidor rodando em http://localhost:${port}`);
});