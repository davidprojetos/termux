package com.example.api005.repository;

import com.example.api005.model.Usuario;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface UsuarioRepository extends MongoRepository<Usuario, String> {
    // Métodos de consulta personalizados, se necessário
}
