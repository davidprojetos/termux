// MyFirebaseMessagingService.java
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

/**
 * Nosso serviço que recebe mensagens FCM.
 */
public class MyFirebaseMessagingService extends FirebaseMessagingService {
    private static final String TAG = "FCMService";

    @Override
    public void onMessageReceived(@NonNull RemoteMessage remoteMessage) {
        // Chamado quando a mensagem (data ou notification) é recebida.
        Log.d(TAG, "Mensagem recebida de: " + remoteMessage.getFrom());

        // Se a mensagem contiver payload de dados (data payload).
        if (remoteMessage.getData().size() > 0) {
            Log.d(TAG, "Payload de dados: " + remoteMessage.getData());
            // Você pode processar dados personalizados aqui (p.ex., salvar em DB).
        }

        // Se a mensagem contiver payload de notificação (notification payload).
        if (remoteMessage.getNotification() != null) {
            String titulo = remoteMessage.getNotification().getTitle();
            String corpo = remoteMessage.getNotification().getBody();
            Log.d(TAG, "Notificação – Título: " + titulo + ", Corpo: " + corpo);

            // Exibir notificação local
            enviarNotificacao(titulo, corpo);
        }
    }

    @Override
    public void onNewToken(@NonNull String token) {
        super.onNewToken(token);
        // Chamado quando um novo token é gerado (ou token atualizado).
        Log.d(TAG, "Novo token FCM: " + token);
        // Aqui, faça lógica para enviar esse token ao seu servidor, se necessário.
    }

    /**
     * Método auxiliar para exibir notificação local.
     */
    private void enviarNotificacao(String titulo, String corpo) {
        Intent intent = new Intent(this, MainActivity.class);
        intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);

        PendingIntent pendingIntent = PendingIntent.getActivity(
                this, 0 /* Request code */, intent,
                PendingIntent.FLAG_ONE_SHOT | PendingIntent.FLAG_IMMUTABLE);

        String canalId = "canal_default";
        Uri defaultSound = RingtoneManager.getDefaultUri(RingtoneManager.TYPE_NOTIFICATION);

        NotificationCompat.Builder notificBuilder =
                new NotificationCompat.Builder(this, canalId)
                        .setSmallIcon(R.drawable.ic_notification) // Ícone em res/drawable/ic_notification.png
                        .setContentTitle(titulo)
                        .setContentText(corpo)
                        .setAutoCancel(true)
                        .setSound(defaultSound)
                        .setContentIntent(pendingIntent);

        NotificationManager notificationManager =
                (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);

        // No Android 8.0+ é preciso criar canal de notificação
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            NotificationChannel canal = new NotificationChannel(
                    canalId,
                    "Canal Padrão",
                    NotificationManager.IMPORTANCE_DEFAULT);
            notificationManager.createNotificationChannel(canal);
        }

        notificationManager.notify(0 /* ID da notificação */, notificBuilder.build());
    }
}