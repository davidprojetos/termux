package com.example.api005.service;

import com.example.api005.model.Usuario;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.ParameterizedTypeReference;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpMethod;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.List;

@Service
public class UsuarioServiceImpl implements UsuarioService {

    @Autowired
    private RestTemplate restTemplate;

    private final String BASE_URL = "http://localhost:8080/api/usuarios";

    @Override
    public List<Usuario> listarUsuarios() {
        return restTemplate.exchange(
                BASE_URL,
                HttpMethod.GET,
                null,
                new ParameterizedTypeReference<List<Usuario>>() {}
        ).getBody();
    }

    @Override
    public Usuario criarUsuario(Usuario usuario) {
        return restTemplate.postForObject(BASE_URL, usuario, Usuario.class);
    }

    @Override
    public Usuario buscarUsuarioPorId(String id) {
        String url = BASE_URL + "/" + id;
        return restTemplate.getForObject(url, Usuario.class);
    }

    @Override
    public Usuario atualizarUsuario(String id, Usuario usuarioAtualizado) {
        String url = BASE_URL + "/" + id;
        HttpEntity<Usuario> entity = new HttpEntity<>(usuarioAtualizado);
        return restTemplate.exchange(url, HttpMethod.PUT, entity, Usuario.class).getBody();
    }

    @Override
    public void deletarUsuario(String id) {
        String url = BASE_URL + "/" + id;
        restTemplate.delete(url);
    }
}
