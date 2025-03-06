<?php
header("Content-Type: application/json");

$swagger = [
    'openapi' => '3.0.0', // Defina a versão OpenAPI (você também pode usar 'swagger' => '2.0' se preferir a versão 2.0)
    'info' => [
        'title' => 'Minha API',
        'description' => 'Documentação da minha API',
        'version' => '1.0.0',
    ],
    'tags' => [
        [
            'name' => 'Saudação', // Nome do grupo de rotas
            'description' => 'Rotas relacionadas a saudações e mensagens',
        ],
    ],
    'paths' => [
        '/api/hello' => [
            'get' => [
                'summary' => 'Exemplo de rota GET',
                'tags' => ['Saudação'], // Associa a tag ao grupo de rotas
                'responses' => [
                    '200' => [
                        'description' => 'Resposta bem-sucedida',
                        'content' => [
                            'application/json' => [
                                'schema' => [
                                    'type' => 'object',
                                    'properties' => [
                                        'mensagem' => [
                                            'type' => 'string',
                                            'example' => 'Olá, mundo!',
                                        ],
                                    ],
                                ],
                            ],
                        ],
                    ],
                ],
            ],
        ],
    ],
];

echo json_encode($swagger);
