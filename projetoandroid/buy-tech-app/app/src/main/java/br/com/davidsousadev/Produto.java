package br.com.davidsousadev;

public class Produto {
    private String nome, descricao, foto;
    private double preco;

    public Produto(String nome, String descricao, String foto, double preco) {
        this.nome = nome;
        this.descricao = descricao;
        this.foto = foto;
        this.preco = preco;
    }

    public String getNome() { return nome; }
    public String getDescricao() { return descricao; }
    public String getFoto() { return foto; }
    public double getPreco() { return preco; }
}