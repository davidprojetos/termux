const express = require('express');
const router = express.Router();
const Usuario = require('../models/usuario');

// Rota para obter todos os usuários
router.get('/', async (req, res) => {
  try {
    const usuarios = await Usuario.find();
    res.json(usuarios);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// Rota para obter um usuário pelo ID
router.get('/:id', async (req, res) => {
  try {
    const usuario = await Usuario.findById(req.params.id);
    if (!usuario) {
      return res.status(404).json({ message: 'Usuário não encontrado.' });
    }
    res.json(usuario);
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

// Rota para criar um novo usuário
router.post('/', async (req, res) => {
  const { nome, email, idade } = req.body;

  try {
    const usuario = new Usuario({
      nome,
      email,
      idade
    });

    const novoUsuario = await usuario.save();
    res.status(201).json(novoUsuario);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
});

// Rota para atualizar um usuário pelo ID
router.put('/:id', async (req, res) => {
  const { nome, email, idade } = req.body;

  try {
    const usuarioAtualizado = await Usuario.findByIdAndUpdate(req.params.id, {
      nome,
      email,
      idade
    }, { new: true });

    if (!usuarioAtualizado) {
      return res.status(404).json({ message: 'Usuário não encontrado.' });
    }

    res.json(usuarioAtualizado);
  } catch (err) {
    res.status(400).json({ message: err.message });
  }
});

// Rota para excluir um usuário pelo ID
router.delete('/:id', async (req, res) => {
  try {
    const usuarioExcluido = await Usuario.findByIdAndDelete(req.params.id);
    if (!usuarioExcluido) {
      return res.status(404).json({ message: 'Usuário não encontrado.' });
    }
    res.json({ message: 'Usuário excluído com sucesso.' });
  } catch (err) {
    res.status(500).json({ message: err.message });
  }
});

module.exports = router;
