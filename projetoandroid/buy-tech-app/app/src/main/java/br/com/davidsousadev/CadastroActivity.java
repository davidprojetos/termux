package br.com.davidsousadev;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.*;
import android.util.Log;
import android.view.View;

import org.json.JSONObject;

import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class CadastroActivity extends AppCompatActivity {

    EditText etNome, etEmail, etCpf, etDataNascimento, etTelefone, etCep, etComplemento, etSenha, etConfirmarSenha;
    Button btnCadastrar;
    Button btnVoltar;
    
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_cadastro);
        
        btnVoltar = findViewById(R.id.btnVoltar);

        btnVoltar.setOnClickListener(v -> finish());
        
        etNome = findViewById(R.id.etNome);
        etEmail = findViewById(R.id.etEmail);
        etCpf = findViewById(R.id.etCpf);
        etDataNascimento = findViewById(R.id.etDataNascimento);
        etTelefone = findViewById(R.id.etTelefone);
        etCep = findViewById(R.id.etCep);
        etComplemento = findViewById(R.id.etComplemento);
        etSenha = findViewById(R.id.etSenha);
        etConfirmarSenha = findViewById(R.id.etConfirmarSenha);
        btnCadastrar = findViewById(R.id.btnCadastrar);

        btnCadastrar.setOnClickListener(v -> cadastrarUsuario());
    }

    private void cadastrarUsuario() {
        new Thread(() -> {
            try {
                URL url = new URL("https://api-buy-tech.vercel.app/clientes/cadastrar"); 
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                conn.setRequestMethod("POST");
                conn.setRequestProperty("Content-Type", "application/json");
                conn.setRequestProperty("accept", "application/json");
                conn.setDoOutput(true);

                JSONObject body = new JSONObject();
                body.put("nome", etNome.getText().toString());
                body.put("email", etEmail.getText().toString());
                body.put("cpf", etCpf.getText().toString());
                body.put("data_nascimento", etDataNascimento.getText().toString());
                body.put("telefone", etTelefone.getText().toString());
                body.put("cep", Integer.parseInt(etCep.getText().toString()));
                body.put("complemento", etComplemento.getText().toString());
                body.put("password", etSenha.getText().toString());
                body.put("confirm_password", etConfirmarSenha.getText().toString());

                OutputStream os = conn.getOutputStream();
                os.write(body.toString().getBytes());
                os.flush();

                int responseCode = conn.getResponseCode();
                Log.d("Cadastro", "Response Code: " + responseCode);

                runOnUiThread(() -> {
                    if (responseCode == 200 || responseCode == 201) {
                        Toast.makeText(CadastroActivity.this, "Cadastro realizado!", Toast.LENGTH_SHORT).show();
                        finish();
                    } else {
                        Toast.makeText(CadastroActivity.this, "Erro no cadastro", Toast.LENGTH_SHORT).show();
                    }
                });

                conn.disconnect();
            } catch (Exception e) {
                e.printStackTrace();
                runOnUiThread(() -> Toast.makeText(CadastroActivity.this, "Falha: " + e.getMessage(), Toast.LENGTH_LONG).show());
            }
        }).start();
    }
}