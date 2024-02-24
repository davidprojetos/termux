package com.example.app.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class MeuController {

    @GetMapping("/")
    public String minhaAcao(Model model) {
        model.addAttribute("mensagem", "Olá, Mundo!");
        return "index";
    }
}
