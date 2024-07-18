package com.example.api005.service;

import com.example.api005.model.Usuario;

import java.util.List;

public interface UsuarioService {

    List<Usuario> listarUsuarios();

    Usuario criarUsuario(Usuario usuario);

    Usuario buscarUsuarioPorId(String id);

    Usuario atualizarUsuario(String id, Usuario usuarioAtualizado);

    void deletarUsuario(String id);
}
