<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Download de Áudio do YouTube</title>
</head>
<body>
    <h2>Insira a URL do vídeo do YouTube para baixar o áudio:</h2>
    <form action="<?php echo $_SERVER['PHP_SELF']; ?>" method="post">
        <input type="text" name="url" placeholder="URL do vídeo">
        <button type="submit">Baixar Áudio</button>
    </form>

    <?php
    if(isset($_POST['url'])) {
        $url = $_POST['url'];
        $output = shell_exec("youtube-dl --extract-audio --audio-format mp3 -o '/data/data/com.termux/files/home/storage/shared/Music/%(title)s.%(ext)s' $url");
        echo "<pre>$output</pre>";
    }
    ?>
</body>
</html>
