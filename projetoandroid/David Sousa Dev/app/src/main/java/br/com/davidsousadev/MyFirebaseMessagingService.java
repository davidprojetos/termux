package br.com.davidsousadev;

import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.media.RingtoneManager;
import android.net.Uri;
import android.os.Build;
import android.util.Log;

import androidx.annotation.NonNull;
import androidx.core.app.NotificationCompat;

import com.google.firebase.messaging.FirebaseMessagingService;
import com.google.firebase.messaging.RemoteMessage;

public class MyFirebaseMessagingService extends FirebaseMessagingService {
    private static final String TAG = "FCMService";

    @Override
    public void onMessageReceived(@NonNull RemoteMessage remoteMessage) {
        Log.d(TAG, "Mensagem recebida de: " + remoteMessage.getFrom());

        String titulo = null;
        String corpo = null;
        String tipo = null;
        String idMensagem = null;
        String url = null;

        if (remoteMessage.getNotification() != null) {
            titulo = remoteMessage.getNotification().getTitle();
            corpo = remoteMessage.getNotification().getBody();
        }

        if (!remoteMessage.getData().isEmpty()) {
            Log.d(TAG, "Payload de dados: " + remoteMessage.getData());
            tipo = remoteMessage.getData().get("tipo");
            idMensagem = remoteMessage.getData().get("id_mensagem");
            url = remoteMessage.getData().get("url");
        }

        enviarNotificacao(
                titulo != null ? titulo : "Nova mensagem",
                corpo != null ? corpo : "Você recebeu uma notificação",
                tipo,
                idMensagem,
                url
        );
    }

    @Override
    public void onNewToken(@NonNull String token) {
        super.onNewToken(token);
        Log.d(TAG, "Novo token FCM: " + token);
    }

    private void enviarNotificacao(String titulo, String corpo, String tipo, String idMensagem, String url) {
        Intent intent;

        if ("mensagem".equals(tipo)) {
            intent = new Intent(this, ChatActivity.class);
        } else {
            intent = new Intent(this, MainActivity.class);
        }

        intent.putExtra("tipo", tipo);
        intent.putExtra("id_mensagem", idMensagem);
        intent.putExtra("url", url);
        intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP | Intent.FLAG_ACTIVITY_NEW_TASK);

        PendingIntent pendingIntent = PendingIntent.getActivity(
                this, 0, intent,
                PendingIntent.FLAG_ONE_SHOT | PendingIntent.FLAG_IMMUTABLE
        );

        String canalId = "canal_default";
        Uri defaultSound = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION);

        NotificationCompat.Builder notificBuilder =
                new NotificationCompat.Builder(this, canalId)
                        .setSmallIcon(R.drawable.ic_notification)
                        .setContentTitle(titulo)
                        .setContentText(corpo)
                        .setStyle(new NotificationCompat.BigTextStyle().bigText(corpo))
                        .setAutoCancel(true)
                        .setSound(defaultSound)
                        .setContentIntent(pendingIntent)
                        .setPriority(NotificationCompat.PRIORITY_HIGH);

        NotificationManager notificationManager =
                (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            NotificationChannel canal = new NotificationChannel(
                    canalId,
                    "Canal Padrão",
                    NotificationManager.IMPORTANCE_HIGH
            );
            notificationManager.createNotificationChannel(canal);
        }

        notificationManager.notify((int) System.currentTimeMillis(), notificBuilder.build());
    }
}