package com.example.apifire;

import android.os.Bundle;
import android.content.Intent;

import androidx.appcompat.app.AppCompatActivity;
import com.google.android.material.bottomnavigation.BottomNavigationView;

import androidx.annotation.Nullable;
import androidx.appcompat.app.AppCompatActivity;

public class PortfolioActivity extends AppCompatActivity {
    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_portfolio);

        // Configura o BottomNavigationView
        BottomNavigationView bottomNavigationView = findViewById(R.id.bottom_navigation);
        bottomNavigationView.setSelectedItemId(R.id.menu_portfolio); // Define o item selecionado

        bottomNavigationView.setOnNavigationItemSelectedListener(item -> {
            if (item.getItemId() == R.id.menu_formacao) {
                startActivity(new Intent(PortfolioActivity.this, FormattingActivity.class));
                finish(); // Encerra a atividade atual para evitar pilha de navegação
                return true;
            } else if (item.getItemId() == R.id.menu_contato) {
                startActivity(new Intent(PortfolioActivity.this, ContactActivity.class));
                finish(); // Encerra a atividade atual para evitar pilha de navegação
                return true;
            } else if (item.getItemId() == R.id.menu_home) {
                startActivity(new Intent(PortfolioActivity.this, MainActivity.class));
                finish(); // Encerra a atividade atual para evitar pilha de navegação
                return true;
            }
            return false;
        });
    }
}

