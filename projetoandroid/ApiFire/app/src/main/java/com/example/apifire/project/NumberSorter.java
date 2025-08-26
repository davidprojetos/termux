package com.example.apifire.project;

import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;
import android.widget.TextView;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

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
