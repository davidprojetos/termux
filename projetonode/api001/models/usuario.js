const mongoose = require('mongoose');

const usuarioSchema = new mongoose.Schema({
  nome: String,
  email: String,
  idade: Number
});

module.exports = mongoose.model('Usuario', usuarioSchema);

