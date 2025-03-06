<?php

header("Content-Type: application/json");

require __DIR__ . '/vendor/autoload.php';

$uri = $_SERVER['REQUEST_URI'];
$method = $_SERVER['REQUEST_METHOD'];

// Simples roteador
if ($uri == '/api/hello' && $method == 'GET') {
    echo json_encode(["message" => "Olá, mundo!"]);
} else {
    http_response_code(404);
    echo json_encode(["error" => "Rota não encontrada"]);
}

