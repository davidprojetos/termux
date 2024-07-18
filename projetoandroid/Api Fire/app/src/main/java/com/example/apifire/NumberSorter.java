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

public class NumberSorter {

    private TextView textViewUltimoSorteado;
    private ListView listViewNumerosSorteados;
    private Button buttonSortear;
    private List<Integer> numerosSorteados = new ArrayList<>();
    private ArrayAdapter<Integer> sorteioAdapter;

    public NumberSorter(TextView textViewUltimoSorteado, ListView listViewNumerosSorteados, Button buttonSortear) {
        this.textViewUltimoSorteado = textViewUltimoSorteado;
        this.listViewNumerosSorteados = listViewNumerosSorteados;
        this.buttonSortear = buttonSortear;

        sorteioAdapter = new ArrayAdapter<>(textViewUltimoSorteado.getContext(), android.R.layout.simple_list_item_1, numerosSorteados);
        listViewNumerosSorteados.setAdapter(sorteioAdapter);

        buttonSortear.setOnClickListener(v -> sortearNumero());
    }

    private void sortearNumero() {
        Random random = new Random();
        int numeroSorteado = random.nextInt(100) + 1;

        numerosSorteados.add(numeroSorteado);
        sorteioAdapter.notifyDataSetChanged();
        textViewUltimoSorteado.setText("Último Número Sorteado: " + numeroSorteado);
    }
}
