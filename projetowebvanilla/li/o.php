<?php

require 'vendor/autoload.php';

use YouTube\YouTubeDownloader;

// Verifica se uma URL foi enviada
if (!isset($_POST['url'])) {
    echo 'Por favor, insira a URL do vídeo do YouTube.';
    exit;
}

// Obtém a URL do vídeo do formulário
$url = $_POST['url'];

// Cria uma instância do downloader
$downloader = new YouTubeDownloader();

try {
    // Obtém o link de download do áudio
    $audioLink = $downloader->getDownloadLink($url, 'audio');

    // Exibe o link de download do áudio
    echo '<a href="' . $audioLink . '" target="_blank">Link de Áudio</a>';
} catch (Exception $e) {
    echo 'Ocorreu um erro ao obter o link de download do áudio: ' . $e->getMessage();
}
