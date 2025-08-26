package com.example.apifire.project;

import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.content.Context;
import android.os.Build;
import android.os.Handler;
import android.os.Looper;
import android.util.Log;

import androidx.core.app.NotificationCompat;

import com.example.apifire.models.BiblePassage;
import com.example.apifire.R;

import java.util.List;
import java.util.Random;

public class BiblePassageNotifier {

    private static final String CHANNEL_ID = "bible_passage_channel";
    private Context context;
    private List<BiblePassage> biblePassages;
    private Handler handler;
    private Runnable notificationRunnable;

    public BiblePassageNotifier(Context context, List<BiblePassage> biblePassages) {
        this.context = context;
        this.biblePassages = biblePassages;
        this.handler = new Handler(Looper.getMainLooper());
        createNotificationChannel();
    }

    private void createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            CharSequence name = "Bible Passage Channel";
            String description = "Channel for Bible passage notifications";
            int importance = NotificationManager.IMPORTANCE_DEFAULT;
            NotificationChannel channel = new NotificationChannel(CHANNEL_ID, name, importance);
            channel.setDescription(description);
            NotificationManager notificationManager = context.getSystemService(NotificationManager.class);
            notificationManager.createNotificationChannel(channel);
        }
    }

    public void startNotifications(long intervalMillis) {
        notificationRunnable = new Runnable() {
            @Override
            public void run() {
                sendNotification();
                handler.postDelayed(this, intervalMillis);
            }
        };
        handler.post(notificationRunnable);
    }

    private void sendNotification() {
        Random random = new Random();
        BiblePassage passage = biblePassages.get(random.nextInt(biblePassages.size()));

        NotificationCompat.Builder builder = new NotificationCompat.Builder(context, CHANNEL_ID)
                .setSmallIcon(R.drawable.ic_notification) // Certifique-se de ter um ícone adequado no seu projeto
                .setContentTitle(passage.getTitle())
                .setContentText(passage.getPassage())
                .setPriority(NotificationCompat.PRIORITY_DEFAULT);

        NotificationManager notificationManager = (NotificationManager) context.getSystemService(Context.NOTIFICATION_SERVICE);

        try {
            if (notificationManager != null) {
                notificationManager.notify(random.nextInt(), builder.build());
            }
        } catch (Exception e) {
            Log.e("BiblePassageNotifier", "Error sending notification", e);
        }
    }

    public void stopNotifications() {
        if (handler != null && notificationRunnable != null) {
            handler.removeCallbacks(notificationRunnable);
            notificationRunnable = null; // Limpa a referência ao Runnable
        }
    }
}
