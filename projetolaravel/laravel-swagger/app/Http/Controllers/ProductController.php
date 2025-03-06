<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use OpenApi\Attributes as OA;
use App\Models\Product;

class ProductController extends Controller
{
    #[OA\Get(
        path: "/api/products",
        summary: "Lista todos os produtos",
        tags: ["Products"],
        responses: [
            new OA\Response(
                response: 200,
                description: "Lista de produtos",
                content: new OA\JsonContent(
                    type: "array",
                    items: new OA\Items(
                        type: "object",
                        properties: [
                            new OA\Property(property: "id", type: "integer", example: 1),
                            new OA\Property(property: "name", type: "string", example: "Produto 1"),
                            new OA\Property(property: "price", type: "number", format: "float", example: 100.0),
                        ]
                    )
                )
            )
        ]
    )]
    public function index()
    {
        return response()->json(Product::all());
    }

    #[OA\Post(
        path: "/api/products",
        summary: "Cria um novo produto",
        tags: ["Products"],
        requestBody: new OA\RequestBody(
            content: new OA\JsonContent(
                required: ["name", "price"],
                properties: [
                    new OA\Property(property: "name", type: "string", example: "Novo Produto"),
                    new OA\Property(property: "price", type: "number", format: "float", example: 150.0),
                ]
            )
        ),
        responses: [
            new OA\Response(response: 201, description: "Produto criado com sucesso"),
            new OA\Response(response: 400, description: "Requisição inválida")
        ]
    )]
    public function store(Request $request)
    {
        $validated = $request->validate([
            'name' => 'required|string|max:255',
            'price' => 'required|numeric',
        ]);

        $product = Product::create($validated);

        return response()->json($product, 201);
    }

    #[OA\Get(
        path: "/api/products/{id}",
        summary: "Exibe um produto específico",
        tags: ["Products"],
        parameters: [
            new OA\Parameter(name: "id", in: "path", required: true, description: "ID do produto",
                schema: new OA\Schema(type: "integer", example: 1))
        ],
        responses: [
            new OA\Response(
                response: 200,
                description: "Produto encontrado",
                content: new OA\JsonContent(
                    type: "object",
                    properties: [
                        new OA\Property(property: "id", type: "integer", example: 1),
                        new OA\Property(property: "name", type: "string", example: "Produto 1"),
                        new OA\Property(property: "price", type: "number", format: "float", example: 100.0),
                    ]
                )
            ),
            new OA\Response(response: 404, description: "Produto não encontrado")
        ]
    )]
    public function show($id)
    {
        $product = Product::find($id);

        if (!$product) {
            return response()->json(['message' => 'Produto não encontrado'], 404);
        }

        return response()->json($product);
    }

    #[OA\Put(
        path: "/api/products/{id}",
        summary: "Atualiza um produto específico",
        tags: ["Products"],
        parameters: [
            new OA\Parameter(name: "id", in: "path", required: true, description: "ID do produto",
                schema: new OA\Schema(type: "integer", example: 1))
        ],
        requestBody: new OA\RequestBody(
            content: new OA\JsonContent(
                required: ["name", "price"],
                properties: [
                    new OA\Property(property: "name", type: "string", example: "Produto Atualizado"),
                    new OA\Property(property: "price", type: "number", format: "float", example: 150.0),
                ]
            )
        ),
        responses: [
            new OA\Response(response: 200, description: "Produto atualizado com sucesso"),
            new OA\Response(response: 400, description: "Requisição inválida"),
            new OA\Response(response: 404, description: "Produto não encontrado")
        ]
    )]
    public function update(Request $request, $id)
    {
        $product = Product::find($id);

        if (!$product) {
            return response()->json(['message' => 'Produto não encontrado'], 404);
        }

        $validated = $request->validate([
            'name' => 'required|string|max:255',
            'price' => 'required|numeric',
        ]);

        $product->update($validated);

        return response()->json($product);
    }
/*
    #[OA\Patch(
        path: "/api/products/{id}",
        summary: "Atualiza parcialmente um produto específico",
        tags: ["Products"],
        parameters: [
            new OA\Parameter(name: "id", in: "path", required: true, description: "ID do produto",
                schema: new OA\Schema(type: "integer", example: 1))
        ],
        requestBody: new OA\RequestBody(
            content: new OA\JsonContent(
                required: ["name", "price"],
                properties: [
                    new OA\Property(property: "name", type: "string", example: "Produto Parcialmente Atualizado"),
                    new OA\Property(property: "price", type: "number", format: "float", example: 125.0),
                ]
            )
        ),
        responses: [
            new OA\Response(response: 200, description: "Produto parcialmente atualizado com sucesso"),
            new OA\Response(response: 400, description: "Requisição inválida"),
            new OA\Response(response: 404, description: "Produto não encontrado")
        ]
    )]
    public function patch(Request $request, $id)
    {
        $product = Product::find($id);

        if (!$product) {
            return response()->json(['message' => 'Produto não encontrado'], 404);
        }

        $product->update($request->only(['name', 'price']));

        return response()->json($product);
    }
*/
    #[OA\Delete(
        path: "/api/products/{id}",
        summary: "Deleta um produto específico",
        tags: ["Products"],
        parameters: [
            new OA\Parameter(name: "id", in: "path", required: true, description: "ID do produto",
                schema: new OA\Schema(type: "integer", example: 1))
        ],
        responses: [
            new OA\Response(response: 200, description: "Produto deletado com sucesso"),
            new OA\Response(response: 404, description: "Produto não encontrado")
        ]
    )]
    public function destroy($id)
    {
        $product = Product::find($id);

        if (!$product) {
            return response()->json(['message' => 'Produto não encontrado'], 404);
        }

        $product->delete();

        return response()->json(['message' => 'Produto deletado com sucesso']);
    }

    #[OA\Options(
        path: "/api/products",
        summary: "Obtém os métodos HTTP suportados para a API",
        tags: ["Products"],
        responses: [
            new OA\Response(response: 200, description: "Métodos suportados", content: new OA\JsonContent(
                properties: [
                    new OA\Property(property: "allow", type: "string", example: "GET, POST, OPTIONS")
                ]
            ))
        ]
    )]
    public function options()
    {
        return response()->json(['allow' => 'GET, POST, OPTIONS']);
    }

    #[OA\Head(
        path: "/api/products",
        summary: "Obtém informações de cabeçalho para a API",
        tags: ["Products"],
        responses: [
            new OA\Response(response: 200, description: "Informações de cabeçalho", content: new OA\JsonContent())
        ]
    )]
    public function head()
    {
        return response()->json([], 200);
    }
/*
    #[OA\Trace(
        path: "/api/products",
        summary: "Rastreia as requisições feitas para a API",
        tags: ["Products"],
        responses: [
            new OA\Response(response: 200, description: "Rastreamento realizado")
        ]
    )]
    public function trace()
    {
        // Trace logic if needed
        return response()->json(['message' => 'Trace realizado'], 200);
    }*/
}
