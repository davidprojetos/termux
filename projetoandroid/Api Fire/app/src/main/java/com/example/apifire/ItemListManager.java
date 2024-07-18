package com.example.apifire;

import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.Locale; // Adicionando a importação de Locale


import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;
import retrofit2.Retrofit;
import retrofit2.converter.gson.GsonConverterFactory;

public class ItemListManager {

    private ListView listViewItems;
    private ArrayAdapter<String> itemAdapter;
    private List<Item> itemList = new ArrayList<>();
    private Item selectedItem;
    private EditText editTextId;
    private EditText editTextNome;
    private Button buttonAdicionar;
    private Button buttonAtualizar;
    private Button buttonDeletar;
    private ApiService apiService;

    public ItemListManager(ListView listViewItems, EditText editTextId, EditText editTextNome,
                           Button buttonAdicionar, Button buttonAtualizar, Button buttonDeletar, Fragment fragment) {
        this.listViewItems = listViewItems;
        this.editTextId = editTextId;
        this.editTextNome = editTextNome;
        this.buttonAdicionar = buttonAdicionar;
        this.buttonAtualizar = buttonAtualizar;
        this.buttonDeletar = buttonDeletar;

        itemAdapter = new ArrayAdapter<>(fragment.requireContext(), android.R.layout.simple_list_item_1);
        listViewItems.setAdapter(itemAdapter);

        buttonAdicionar.setOnClickListener(v -> adicionarItem());
        buttonAtualizar.setOnClickListener(v -> atualizarItem());
        buttonDeletar.setOnClickListener(v -> deletarItem());

        listViewItems.setOnItemClickListener((parent, view, position, id) -> {
            selectedItem = itemList.get(position);
            editTextId.setText(selectedItem.getId());
            editTextNome.setText(selectedItem.getNome());
        });

        Retrofit retrofit = new Retrofit.Builder()
                .baseUrl("https://different-mewing-manchego.glitch.me/")
                .addConverterFactory(GsonConverterFactory.create())
                .build();

        apiService = retrofit.create(ApiService.class);
        fetchItems();
    }

    private void fetchItems() {
        Call<List<Item>> call = apiService.getItems();
        call.enqueue(new Callback<List<Item>>() {
            @Override
            public void onResponse(Call<List<Item>> call, Response<List<Item>> response) {
                if (response.isSuccessful()) {
                    List<Item> items = response.body();
                    if (items != null) {
                        itemList.clear();
                        itemList.addAll(items);
                        itemAdapter.clear();
                        for (Item item : items) {
                            itemAdapter.add(item.getNome());
                        }
                    }
                } else {
                    Toast.makeText(listViewItems.getContext(), "Erro ao obter lista de itens: " + response.message(), Toast.LENGTH_SHORT).show();
                }
            }

            @Override
            public void onFailure(Call<List<Item>> call, Throwable t) {
                Toast.makeText(listViewItems.getContext(), "Falha na requisição: " + t.getMessage(), Toast.LENGTH_SHORT).show();
            }
        });
    }

    private void adicionarItem() {
        String nome = editTextNome.getText().toString().trim();
        if (!nome.isEmpty()) {
            Item newItem = new Item();
            newItem.setNome(nome);

            Call<Item> call = apiService.createItem(newItem);
            call.enqueue(new Callback<Item>() {
                @Override
                public void onResponse(Call<Item> call, Response<Item> response) {
                    if (response.isSuccessful()) {
                        Toast.makeText(listViewItems.getContext(), "Item adicionado com sucesso", Toast.LENGTH_SHORT).show();
                        editTextId.setText("");
                        editTextNome.setText("");
                        fetchItems();
                    } else {
                        Toast.makeText(listViewItems.getContext(), "Erro ao adicionar item: " + response.message(), Toast.LENGTH_SHORT).show();
                    }
                }

                @Override
                public void onFailure(Call<Item> call, Throwable t) {
                    Toast.makeText(listViewItems.getContext(), "Falha na requisição: " + t.getMessage(), Toast.LENGTH_SHORT).show();
                }
            });
        } else {
            Toast.makeText(listViewItems.getContext(), "Nome do item não pode ser vazio", Toast.LENGTH_SHORT).show();
        }
    }

    private void atualizarItem() {
        String id = editTextId.getText().toString().trim();
        String nome = editTextNome.getText().toString().trim();
        if (!id.isEmpty() && !nome.isEmpty()) {
            Item updatedItem = new Item();
            updatedItem.setId(id);
            updatedItem.setNome(nome);

            Call<Item> call = apiService.updateItem(id, updatedItem);
            call.enqueue(new Callback<Item>() {
                @Override
                public void onResponse(Call<Item> call, Response<Item> response) {
                    if (response.isSuccessful()) {
                        Toast.makeText(listViewItems.getContext(), "Item atualizado com sucesso", Toast.LENGTH_SHORT).show();
                        editTextId.setText("");
                        editTextNome.setText("");
                        fetchItems();
                    } else {
                        Toast.makeText(listViewItems.getContext(), "Erro ao atualizar item: " + response.message(), Toast.LENGTH_SHORT).show();
                    }
                }

                @Override
                public void onFailure(Call<Item> call, Throwable t) {
                    Toast.makeText(listViewItems.getContext(), "Falha na requisição: " + t.getMessage(), Toast.LENGTH_SHORT).show();
                }
            });
        } else {
            Toast.makeText(listViewItems.getContext(), "ID e nome do item não podem ser vazios", Toast.LENGTH_SHORT).show();
        }
    }

    private void deletarItem() {
        String id = editTextId.getText().toString().trim();
        if (!id.isEmpty()) {
            Call<Void> call = apiService.deleteItem(id);
            call.enqueue(new Callback<Void>() {
                @Override
                public void onResponse(Call<Void> call, Response<Void> response) {
                    if (response.isSuccessful()) {
                        Toast.makeText(listViewItems.getContext(), "Item deletado com sucesso", Toast.LENGTH_SHORT).show();
                        editTextId.setText("");
                        editTextNome.setText("");
                        fetchItems();
                    } else {
                        Toast.makeText(listViewItems.getContext(), "Erro ao deletar item: " + response.message(), Toast.LENGTH_SHORT).show();
                    }
                }

                @Override
                public void onFailure(Call<Void> call, Throwable t) {
                    Toast.makeText(listViewItems.getContext(), "Falha na requisição: " + t.getMessage(), Toast.LENGTH_SHORT).show();
                }
            });
        } else {
            Toast.makeText(listViewItems.getContext(), "ID do item não pode ser vazio", Toast.LENGTH_SHORT).show();
        }
    }
}
