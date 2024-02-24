package com.example.demo;

import org.springframework.data.jpa.repository.JpaRepository;

public interface CrudRepository extends JpaRepository<Registro, Long> {
    // Adicione métodos de consulta personalizados, se necessário
}
