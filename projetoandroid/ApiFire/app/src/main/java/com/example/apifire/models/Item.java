package com.example.apifire.models;

import com.google.gson.annotations.SerializedName;

public class Item {
    @SerializedName("_id")
    private String id;

    @SerializedName("Nome")
    private String nome;

    // Getters e Setters
    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getNome() {
        return nome;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }
}
