<?php
function getPayload() {
    return json_decode(file_get_contents('php://input'), true);
}

function sendResponse($data, $statusCode = 200) {
    http_response_code($statusCode);
    header('Content-Type: application/json');
    echo json_encode($data);
    exit;
}
