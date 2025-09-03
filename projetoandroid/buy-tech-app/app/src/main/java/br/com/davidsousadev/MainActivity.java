package br.com.davidsousadev;

import androidx.appcompat.app.AppCompatActivity;
import androidx.annotation.NonNull;
import androidx.core.app.ActivityCompat;
import androidx.core.content.ContextCompat;

import android.Manifest;
import android.content.pm.PackageManager;
import android.os.Build;
import android.os.Bundle;
import android.util.Log;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.messaging.FirebaseMessaging;

public class MainActivity extends AppCompatActivity {
    private static final String TAG = "MainActivityFCM";
    private static final int REQUEST_CODE_NOTIFICATIONS = 1001;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main); // layout limpo

        // 🔹 Solicita permissão de notificação no Android 13+
        requestNotificationPermission();

        // 🔹 Apenas loga o token atual (debug), não envia ao backend
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
            }
        }
    }

    @Override
    protected void onNewIntent(android.content.Intent intent) {
        super.onNewIntent(intent);
        setIntent(intent);
        handleNotificationIntent();
    }
}