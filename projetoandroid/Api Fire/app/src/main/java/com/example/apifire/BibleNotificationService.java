package com.example.apifire;

import android.app.Notification;
import android.app.Service;
import android.content.Intent;
import android.os.IBinder;

import androidx.annotation.Nullable;

public class BibleNotificationService extends Service {

    private BibleNotificationManager bibleNotificationManager;

    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        // Iniciar o serviço em modo de primeiro plano
        bibleNotificationManager = new BibleNotificationManager();
        bibleNotificationManager.showNotification(this, "Your notification message");
        return START_STICKY;
    }
}
