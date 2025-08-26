package com.example.apifire.managers;

import android.content.Context;
import android.content.Intent;
import android.net.Uri;

public class QuizzManager {
    private Context context;

    public QuizzManager(Context context) {
        this.context = context;
    }

    public void abrirWebView() {
        Intent browserIntent = new Intent(Intent.ACTION_VIEW, Uri.parse("https://david-ds.rf.gd/sistema-questoes/"));
        context.startActivity(browserIntent);
    }
}
