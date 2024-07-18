package com.example.apifire;

import com.example.apifire.PomodoroTimer;
import com.example.apifire.NumberSorter;
import com.example.apifire.ItemListManager;

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

public class JogoVelhaFragment extends Fragment {

    private Button[] buttons = new Button[9];
    private boolean player1Turn = true; // True para X, False para O

    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container, Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_jogo_velha, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        // Inicialização dos botões
        for (int i = 0; i < buttons.length; i++) {
            String buttonId = "button" + (i + 1);
            int resId = getResources().getIdentifier(buttonId, "id", requireActivity().getPackageName());
            buttons[i] = view.findViewById(resId);
        }
    }

    public void onButtonClick(View view) {
        Button button = (Button) view;
        if (button.getText().toString().isEmpty()) {
            if (player1Turn) {
                button.setText("X");
            } else {
                button.setText("O");
            }
            player1Turn = !player1Turn;
            checkForWin();
        }
    }

    private void checkForWin() {
        // Lógica para verificar se houve um vencedor
        // Exemplo simples: Verificar todas as combinações de vitória
        // Implemente sua própria lógica de verificação aqui
    }

    // Métodos adicionais conforme necessário para o jogo
}
