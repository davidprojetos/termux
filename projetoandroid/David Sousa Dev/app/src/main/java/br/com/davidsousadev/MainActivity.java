package br.com.davidsousadev;

import androidx.appcompat.app.AppCompatActivity;
import androidx.annotation.NonNull;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import android.Manifest;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
import android.content.pm.PackageManager;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;
import android.widget.Toast;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.messaging.FirebaseMessaging;

import br.com.davidsousadev.databinding.ActivityMainBinding;

public class MainActivity extends AppCompatActivity {
    private static final String TAG = "MainActivityFCM";
    private static final int REQUEST_CODE_NOTIFICATIONS = 1001;

    private ActivityMainBinding binding;
    private String currentToken = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        binding = ActivityMainBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());

        // 🔹 Solicita permissão de notificação no Android 13+
        requestNotificationPermission();

        // 🔹 Obtém token FCM
        FirebaseMessaging.getInstance().getToken()
            .addOnCompleteListener(new OnCompleteListener<String>() {
                @Override
                public void onComplete(@NonNull Task<String> task) {
                    if (!task.isSuccessful()) {
                        Log.w(TAG, "Falha ao obter token FCM", task.getException());
                        binding.tokenTextView.setText("Erro ao obter o token.");
                        return;
                    }

                    currentToken = task.getResult();
                    Log.d(TAG, "Token do dispositivo: " + currentToken);
                    binding.tokenTextView.setText("Token do dispositivo:\n" + currentToken);
                }
            });

        // 🔹 Botão para copiar token
        binding.copyTokenButton.setOnClickListener(v -> {
            if (!currentToken.isEmpty()) {
                ClipboardManager clipboard = (ClipboardManager) getSystemService(Context.CLIPBOARD_SERVICE);
                ClipData clip = ClipData.newPlainText("FCM Token", currentToken);
                clipboard.setPrimaryClip(clip);
                Toast.makeText(MainActivity.this, "Token copiado para a área de transferência", Toast.LENGTH_SHORT).show();
            } else {
                Toast.makeText(MainActivity.this, "Token ainda não carregado", Toast.LENGTH_SHORT).show();
            }
        });

        // 🔹 Trata caso a activity seja aberta via notificação
        handleNotificationIntent();
    }

    private void requestNotificationPermission() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) { // Android 13+
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
                Toast.makeText(this, "Aberto por push: tipo=" + tipo + ", id=" + idMensagem, Toast.LENGTH_LONG).show();
            }
        }
    }

    @Override
    protected void onNewIntent(android.content.Intent intent) {
        super.onNewIntent(intent);
        setIntent(intent); // atualiza o intent atual
        handleNotificationIntent();
    }

    @Override
    public void onRequestPermissionsResult(int requestCode,
                                           @NonNull String[] permissions,
                                           @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);

        if (requestCode == REQUEST_CODE_NOTIFICATIONS) {
            if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                Toast.makeText(this, "Permissão de notificações concedida ✅", Toast.LENGTH_SHORT).show();
            } else {
                Toast.makeText(this, "Permissão de notificações negada ❌", Toast.LENGTH_SHORT).show();
            }
        }
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        binding = null;
    }
}