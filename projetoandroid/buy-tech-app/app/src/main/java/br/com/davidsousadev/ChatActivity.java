package br.com.davidsousadev;

import android.content.Intent;
import android.os.AsyncTask;
import android.os.Bundle;
import android.util.Log;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import org.json.JSONArray;
import org.json.JSONObject;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;

import com.bumptech.glide.Glide;

public class ChatActivity extends AppCompatActivity {

    private static final String TAG = "ChatActivity";
    private TextView chatInfo;
    private ImageView productImage;
    private Button backButton;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_chat);

        chatInfo = findViewById(R.id.chatInfoText);
        productImage = findViewById(R.id.productImage);
        backButton = findViewById(R.id.backButton);

        Intent intent = getIntent();
        if (intent != null && intent.getExtras() != null) {
            String idMensagem = intent.getStringExtra("id_mensagem");
            Log.d(TAG, "🔹 ID recebido: " + idMensagem);

            if (idMensagem != null) {
                chatInfo.setText("Buscando produto em promoção...");

                // Buscar dados da API em background
                new FetchProductTask().execute(idMensagem);
            } else {
                chatInfo.setText("Nenhum ID recebido.");
            }
        }

        // Botão voltar
        backButton.setOnClickListener(v -> {
            Intent mainIntent = new Intent(ChatActivity.this, MainActivity.class);
            startActivity(mainIntent);
            finish();
        });
    }

    // Classe para buscar produto em background
    private class FetchProductTask extends AsyncTask<String, Void, String> {
        @Override
        protected String doInBackground(String... params) {
            String idMensagem = params[0];
            try {
                URL url = new URL("https://api-buy-tech.vercel.app/produtos?id=" + idMensagem);
                HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                conn.setRequestMethod("GET");

                BufferedReader reader = new BufferedReader(
                        new InputStreamReader(conn.getInputStream())
                );
                StringBuilder response = new StringBuilder();
                String line;
                while ((line = reader.readLine()) != null) {
                    response.append(line);
                }
                reader.close();
                return response.toString();
            } catch (Exception e) {
                Log.e(TAG, "Erro ao buscar produto", e);
                return null;
            }
        }

@Override
protected void onPostExecute(String result) {
    if (result == null) {
        chatInfo.setText("Erro ao buscar produto.");
        return;
    }

    try {
        JSONArray jsonArray = new JSONArray(result);
        JSONObject product = jsonArray.getJSONObject(0);

        String nome = product.getString("nome");
        String descricao = product.getString("descricao");
        double preco = product.getDouble("preco");
        String foto = product.getString("foto");

        chatInfo.setText(
                "🔥 " + nome + "\n\n" +
                descricao + "\n\n💰 R$ " + preco
        );

        // 🔹 Carregar imagem com Glide
        Glide.with(ChatActivity.this)
                .load(foto)
                .placeholder(R.mipmap.ic_launcher) // imagem temporária
                .error(android.R.drawable.ic_menu_report_image) // se der erro
                .into(productImage);

    } catch (Exception e) {
        Log.e(TAG, "Erro ao processar JSON", e);
        chatInfo.setText("Erro ao processar produto.");
    }
}
    }
}