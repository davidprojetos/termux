package com.example.demo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import org.h2.tools.Server;
import java.sql.SQLException; // Adicione esta importação

import java.sql.Connection;
import java.sql.DriverManager;

@SpringBootApplication
public class DemoApplication {

    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
    }
}

@RestController
class ConnectionController {

    @GetMapping("/verificarConexao")
    public String verificarConexao() {
        try {
            // Configuração para o H2 em memória
            String url = "jdbc:h2:mem:testdb";
            String user = "sa";
            String password = "";

            // Conectar ao H2
            Connection connection = DriverManager.getConnection(url, user, password);

            // Verificar se a conexão foi bem-sucedida
            if (connection != null) {
                connection.close();
                return "Conexão bem-sucedida com o H2!";
            } else {
                return "Falha na conexão com o H2.";
            }

        } catch (Exception e) {
            e.printStackTrace();
            return "Erro ao verificar a conexão com o H2.";
        }
    }
}
