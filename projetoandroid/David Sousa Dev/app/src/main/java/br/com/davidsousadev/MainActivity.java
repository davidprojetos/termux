package br.com.davidsousadev;

import androidx.appcompat.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
import android.widget.Toast;

import androidx.annotation.NonNull;

import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.messaging.FirebaseMessaging;

import br.com.davidsousadev.databinding.ActivityMainBinding;

public class MainActivity extends AppCompatActivity {
    private static final String TAG = "MainActivityFCM";
    private ActivityMainBinding binding;
    private String currentToken = "";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        binding = ActivityMainBinding.inflate(getLayoutInflater());
        setContentView(binding.getRoot());

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
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        binding = null;
    }
}