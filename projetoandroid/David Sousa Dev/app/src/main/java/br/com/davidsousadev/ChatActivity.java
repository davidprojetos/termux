package br.com.davidsousadev;

import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.util.Log;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

public class ChatActivity extends AppCompatActivity {

    private static final String TAG = "ChatActivity";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_chat);

        TextView chatInfo = findViewById(R.id.chatInfoText);

        Intent intent = getIntent();
        if (intent != null && intent.getExtras() != null) {
            String idMensagem = intent.getStringExtra("id_mensagem");
            String tipo = intent.getStringExtra("tipo");
            String url = intent.getStringExtra("url");

            Log.d(TAG, "🔹 Dados recebidos da notificação:");
            Log.d(TAG, "id_mensagem = " + idMensagem);
            Log.d(TAG, "tipo = " + tipo);
            Log.d(TAG, "url = " + url);

            if (idMensagem != null) {
                chatInfo.setText("Abrindo chat da mensagem ID: " + idMensagem);
            } else {
                chatInfo.setText("Nenhuma mensagem encontrada.");
            }

            // Abre URL se enviada
            if (url != null && !url.isEmpty()) {
                Intent browserIntent = new Intent(Intent.ACTION_VIEW, Uri.parse(url));
                startActivity(browserIntent);
            }
        } else {
            chatInfo.setText("Nenhum dado recebido da notificação.");
        }
    }
}