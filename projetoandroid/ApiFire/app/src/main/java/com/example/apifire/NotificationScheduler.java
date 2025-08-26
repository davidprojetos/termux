package com.example.apifire;

import android.app.AlarmManager;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Build;

import androidx.core.app.NotificationCompat;
import androidx.core.app.NotificationManagerCompat;

public class NotificationScheduler {
    private static final String CHANNEL_ID = "scheduled_notification_channel";
    private Context context;

    public NotificationScheduler(Context context) {
        this.context = context;
        createNotificationChannel();
    }

    private void createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            CharSequence name = "Scheduled Notification Channel";
            String description = "Channel for scheduled notifications";
            int importance = NotificationManager.IMPORTANCE_DEFAULT;
            NotificationChannel channel = new NotificationChannel(CHANNEL_ID, name, importance);
            channel.setDescription(description);

            NotificationManager notificationManager = context.getSystemService(NotificationManager.class);
            notificationManager.createNotificationChannel(channel);
        }
    }

    public void scheduleNotification(long triggerAtMillis, int notificationId, String title, String message, int iconResId) {
        Intent intent = new Intent(context, NotificationReceiver.class);
        intent.putExtra("notificationId", notificationId);
        intent.putExtra("title", title);
        intent.putExtra("message", message);
        intent.putExtra("iconResId", iconResId);

        PendingIntent pendingIntent = PendingIntent.getBroadcast(context, notificationId, intent, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
        AlarmManager alarmManager = (AlarmManager) context.getSystemService(Context.ALARM_SERVICE);
        alarmManager.setExact(AlarmManager.RTC_WAKEUP, triggerAtMillis, pendingIntent);
    }

    public static class NotificationReceiver extends BroadcastReceiver {
        @Override
        public void onReceive(Context context, Intent intent) {
            int notificationId = intent.getIntExtra("notificationId", 0);
            String title = intent.getStringExtra("title");
            String message = intent.getStringExtra("message");
            int iconResId = intent.getIntExtra("iconResId", R.drawable.ic_notification);

            NotificationCompat.Builder builder = new NotificationCompat.Builder(context, CHANNEL_ID)
                    .setSmallIcon(iconResId)
                    .setContentTitle(title)
                    .setContentText(message)
                    .setPriority(NotificationCompat.PRIORITY_DEFAULT)
                    .setAutoCancel(true);

            NotificationManagerCompat notificationManager = NotificationManagerCompat.from(context);
            notificationManager.notify(notificationId, builder.build());
        }
    }
}
