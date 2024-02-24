// src/main/kotlin/com/example/controllers/HomeController.kt

package com.example.appkotlin.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
class HelloController {

    @GetMapping("/")
    fun helloWorld(model: Model): String {
        model.addAttribute("mensagem", "Olá, Mundo!")
        return "index" // Isso refere-se a um arquivo de modelo chamado hello-world.html
    }
}
