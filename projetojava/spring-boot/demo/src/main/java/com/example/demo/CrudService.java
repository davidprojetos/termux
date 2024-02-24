package com.example.demo;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class CrudService {

    @Autowired
    private CrudRepository crudRepository;

    public List<Registro> listarRegistros() {
        return crudRepository.findAll();
    }

    public Registro buscarRegistro(Long id) {
        return crudRepository.findById(id).orElse(null);
    }

    public void salvarRegistro(Registro registro) {
        crudRepository.save(registro);
    }

    public void excluirRegistro(Long id) {
        crudRepository.deleteById(id);
    }
}
