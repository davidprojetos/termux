<?php
require 'config.php';
require 'functions.php';

$method = $_SERVER['REQUEST_METHOD'];
$requestUri = explode('/', trim($_SERVER['REQUEST_URI'], '/'));

// API para gerenciar itens
if ($requestUri[0] === 'api' && isset($requestUri[1])) {
    $endpoint = $requestUri[1];
    $id = $requestUri[2] ?? null;

    switch ($endpoint) {
        case 'items':
            if ($method === 'GET') {
                if ($id) {
                    // Retorna um item específico
                    $stmt = $pdo->prepare('SELECT * FROM items WHERE id = ?');
                    $stmt->execute([$id]);
                    $item = $stmt->fetch(PDO::FETCH_ASSOC);
                    sendResponse($item ?: ['error' => 'Item not found'], $item ? 200 : 404);
                } else {
                    // Retorna todos os itens
                    $stmt = $pdo->query('SELECT * FROM items');
                    $items = $stmt->fetchAll(PDO::FETCH_ASSOC);
                    sendResponse($items);
                }
            } elseif ($method === 'POST') {
                // Cria um novo item
                $data = getPayload();
                if (!isset($data['name']) || !isset($data['description'])) {
                    sendResponse(['error' => 'Invalid input'], 400);
                }

                $stmt = $pdo->prepare('INSERT INTO items (name, description) VALUES (?, ?)');
                $stmt->execute([$data['name'], $data['description']]);
                sendResponse(['message' => 'Item created'], 201);
            } elseif ($method === 'PUT' && $id) {
                // Atualiza um item
                $data = getPayload();
                if (!isset($data['name']) || !isset($data['description'])) {
                    sendResponse(['error' => 'Invalid input'], 400);
                }

                $stmt = $pdo->prepare('UPDATE items SET name = ?, description = ? WHERE id = ?');
                $stmt->execute([$data['name'], $data['description'], $id]);
                sendResponse(['message' => 'Item updated']);
            } elseif ($method === 'DELETE' && $id) {
                // Deleta um item
                $stmt = $pdo->prepare('DELETE FROM items WHERE id = ?');
                $stmt->execute([$id]);
                sendResponse(['message' => 'Item deleted']);
            } else {
                sendResponse(['error' => 'Method not allowed'], 405);
            }
            break;

        default:
            sendResponse(['error' => 'Endpoint not found'], 404);
    }
} else {
    sendResponse(['error' => 'Invalid API route'], 404);
}

