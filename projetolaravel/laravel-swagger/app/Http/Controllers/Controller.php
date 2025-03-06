<?php
namespace App\Http\Controllers;
use OpenApi\Attributes as OA;

#[OA\Info(
title: "Minha primeira API Laravel 12 / swagger", 
version: "0.1"
)]

#[OA\Server(
    url: "http://127.0.0.1:8000",
    description: "Servidor API"
)]
abstract class Controller
{
    //
}
