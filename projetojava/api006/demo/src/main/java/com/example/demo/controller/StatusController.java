package com.example.demo.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class StatusController {

    @Autowired
    private JdbcTemplate jdbcTemplate;

    @GetMapping("/status")
    public String checkStatus() {
        String result;
        try {
            jdbcTemplate.queryForObject("SELECT 1", Integer.class);
            result = "Conexão com o banco de dados estabelecida com sucesso.";
        } catch (Exception e) {
            result = "Erro ao conectar ao banco de dados: " + e.getMessage();
        }
        return result;
    }
}
