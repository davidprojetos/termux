const express = require('express');
const ytdl = require('ytdl-core');
const fs = require('fs');

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

        res.header('Content-Disposition', `attachment; filename="${info.videoDetails.title}.mp3"`);
        ytdl(url, { format: audioFormat })
            .pipe(fs.createWriteStream(`${info.videoDetails.title}.mp3`))
            .on('finish', () => {
                console.log('Download concluído!');
                res.download(`${info.videoDetails.title}.mp3`, () => {
                    fs.unlinkSync(`${info.videoDetails.title}.mp3`);
                });
            });
    } catch (error) {
        console.error('Erro ao fazer o download:', error);
        res.status(500).send('Erro ao fazer o download');
    }
});

app.listen(port, () => {
    console.log(`Servidor rodando em http://localhost:${port}`);
});
