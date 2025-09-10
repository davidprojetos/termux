package br.com.davidsousadev;

import androidx.appcompat.app.AppCompatActivity;
import androidx.annotation.NonNull;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import android.Manifest;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;
import android.widget.ImageView;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.messaging.FirebaseMessaging;

import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import okhttp3.Call;
import okhttp3.Callback;
import okhttp3.OkHttpClient;
import okhttp3.Request;
import okhttp3.Response;

public class MainActivity extends AppCompatActivity {
    private static final String TAG = "MainActivityFCM";
    private static final int REQUEST_CODE_NOTIFICATIONS = 1001;

    private TextView tvStatus;
    private ImageView ivUser;
    private ProgressBar progressBar;
    private RecyclerView rvProdutos;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        // 🔹 Views
        tvStatus = findViewById(R.id.tvStatus);
        ivUser = findViewById(R.id.ivUser);
        progressBar = findViewById(R.id.progressBar);
        rvProdutos = findViewById(R.id.rvProdutos);

        // 🔹 Permissão de notificação no Android 13+
        requestNotificationPermission();

        // 🔹 Trata abertura por push notification
        handleNotificationIntent();

        // 🔹 Checa se usuário já está logado
        verificarLogin();

        // 🔹 Ícone de usuário clicável
        ivUser.setOnClickListener(v -> {
            SharedPreferences prefs = getSharedPreferences("MyAppPrefs", MODE_PRIVATE);
            String token = prefs.getString("userToken", null);

            if (token != null) {
                // Usuário logado → desloga
                prefs.edit().remove("userToken").apply();
                verificarLogin();
                Toast.makeText(this, "Logout realizado", Toast.LENGTH_SHORT).show();
            } else {
                // Usuário não logado → abrir login
                startActivity(new Intent(MainActivity.this, LoginActivity.class));
            }
        });

        // 🔹 Carregar produtos da API
        carregarProdutos();

        // 🔹 Loga o token FCM (apenas debug)
        FirebaseMessaging.getInstance().getToken()
            .addOnCompleteListener(new OnCompleteListener<String>() {
                @Override
                public void onComplete(@NonNull Task<String> task) {
                    if (!task.isSuccessful()) {
                        Log.w(TAG, "Falha ao obter token FCM", task.getException());
                        return;
                    }
                    String token = task.getResult();
                    Log.d(TAG, "Token atual (debug): " + token);
                }
            });
    }

    private void verificarLogin() {
        SharedPreferences prefs = getSharedPreferences("MyAppPrefs", MODE_PRIVATE);
        String token = prefs.getString("userToken", null);

        if (token != null) {
            tvStatus.setText("Usuário autenticado ✅");
            ivUser.setColorFilter(ContextCompat.getColor(this, R.color.teal_700));
        } else {
            tvStatus.setText("Nenhum usuário logado");
            ivUser.setColorFilter(ContextCompat.getColor(this, R.color.black));
        }
    }

    private void requestNotificationPermission() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.POST_NOTIFICATIONS)
                    != PackageManager.PERMISSION_GRANTED) {
                ActivityCompat.requestPermissions(this,
                        new String[]{Manifest.permission.POST_NOTIFICATIONS},
                        REQUEST_CODE_NOTIFICATIONS);
            }
        }
    }

    private void handleNotificationIntent() {
        if (getIntent() != null && getIntent().getExtras() != null) {
            String tipo = getIntent().getStringExtra("tipo");
            String idMensagem = getIntent().getStringExtra("id_mensagem");
            if (tipo != null) {
                Log.d(TAG, "MainActivity aberta pelo push: tipo=" + tipo + ", id=" + idMensagem);
            }
        }
    }

    @Override
    protected void onNewIntent(Intent intent) {
        super.onNewIntent(intent);
        setIntent(intent);
        handleNotificationIntent();
    }

    @Override
    protected void onResume() {
        super.onResume();
        verificarLogin(); // revalida login sempre que voltar
    }

    private void carregarProdutos() {
        progressBar.setVisibility(ProgressBar.VISIBLE);

        OkHttpClient client = new OkHttpClient();
        Request request = new Request.Builder()
                .url("https://api-buy-tech.vercel.app/produtos")
                .get()
                .build();

        client.newCall(request).enqueue(new Callback() {
            @Override
            public void onFailure(Call call, IOException e) {
                runOnUiThread(() -> {
                    progressBar.setVisibility(ProgressBar.GONE);
                    Toast.makeText(MainActivity.this, "Erro ao carregar produtos", Toast.LENGTH_SHORT).show();
                });
            }

            @Override
            public void onResponse(Call call, Response response) throws IOException {
                String jsonStr = response.body().string();
                try {
                    JSONArray arr = new JSONArray(jsonStr);
                    List<Produto> produtos = new ArrayList<>();
                    for (int i = 0; i < arr.length(); i++) {
                        JSONObject obj = arr.getJSONObject(i);
                        produtos.add(new Produto(
                                obj.getString("nome"),
                                obj.getString("descricao"),
                                obj.getString("foto"),
                                obj.getDouble("preco")
                        ));
                    }

                    runOnUiThread(() -> {
                        progressBar.setVisibility(ProgressBar.GONE);
                        ProdutoAdapter adapter = new ProdutoAdapter(MainActivity.this, produtos);
                        rvProdutos.setAdapter(adapter);
                        rvProdutos.setLayoutManager(new LinearLayoutManager(MainActivity.this));
                    });

                } catch (JSONException e) {
                    e.printStackTrace();
                    runOnUiThread(() -> {
                        progressBar.setVisibility(ProgressBar.GONE);
                        Toast.makeText(MainActivity.this, "Erro ao processar dados", Toast.LENGTH_SHORT).show();
                    });
                }
            }
        });
    }
}