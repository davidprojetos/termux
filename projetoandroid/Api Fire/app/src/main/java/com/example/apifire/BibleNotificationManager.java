package com.example.apifire;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.os.Build;

import androidx.core.app.NotificationCompat;

public class BibleNotificationManager {

    private static final String CHANNEL_ID = "BibleNotifications";
    private static final int NOTIFICATION_ID = 1;

    public void showNotification(Context context, String message) {
        NotificationManager notificationManager = (NotificationManager) context.getSystemService(Context.NOTIFICATION_SERVICE);

        // Criar o canal de notificação se o Android for Oreo ou superior
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            NotificationChannel channel = new NotificationChannel(CHANNEL_ID, "Passagens Bíblicas", NotificationManager.IMPORTANCE_DEFAULT);
            channel.setDescription("Notificações de passagens bíblicas");
            notificationManager.createNotificationChannel(channel);
        }

        // Criar a intenção que será disparada quando o usuário tocar na notificação
        Intent intent = new Intent(context, MainActivity.class);
        intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
        PendingIntent pendingIntent = PendingIntent.getActivity(context, 0, intent, PendingIntent.FLAG_UPDATE_CURRENT);

        // Construir a notificação
        NotificationCompat.Builder builder = new NotificationCompat.Builder(context, CHANNEL_ID)
                .setSmallIcon(R.drawable.ic_notification) // Substitua com o ícone do seu app
                .setContentTitle("Passagem Bíblica")
                .setContentText(message)
                .setPriority(NotificationCompat.PRIORITY_DEFAULT)
                .setContentIntent(pendingIntent)
                .setAutoCancel(true);

        // Mostrar a notificação
        notificationManager.notify(NOTIFICATION_ID, builder.build());
    }
}
