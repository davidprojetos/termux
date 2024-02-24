package com.example.demo.controller;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ResponseBody;

@Controller
public class HomeController {

    @GetMapping("/")
   // @ResponseBody
    public String minhaAcao(Model model) {
        model.addAttribute("mensagem", "Olá, Mundo!");
        return "index";
    }
}
