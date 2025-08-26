package com.example.apifire.project;

import android.os.CountDownTimer;
import android.widget.Button;
import android.widget.TextView;

import java.util.Locale;

public class PomodoroTimer {

    private TextView textViewTimer;
    private Button buttonPlay;
    private Button buttonPause;
    private Button buttonStop;
    private CountDownTimer countDownTimer;
    private boolean isRunning = false;
    private long timeLeftInMillis = 600000; // 25 minutos em milissegundos

    public PomodoroTimer(TextView textViewTimer, Button buttonPlay, Button buttonPause, Button buttonStop) {
        this.textViewTimer = textViewTimer;
        this.buttonPlay = buttonPlay;
        this.buttonPause = buttonPause;
        this.buttonStop = buttonStop;

        buttonPlay.setOnClickListener(v -> startTimer());
        buttonPause.setOnClickListener(v -> pauseTimer());
        buttonStop.setOnClickListener(v -> stopTimer());

        updateTimerText();
    }

    private void startTimer() {
        if (isRunning) return;

        countDownTimer = new CountDownTimer(timeLeftInMillis, 1000) {
            @Override
            public void onTick(long millisUntilFinished) {
                timeLeftInMillis = millisUntilFinished;
                updateTimerText();
            }

            @Override
            public void onFinish() {
                isRunning = false;
                // Adicione aqui o método para tocar o alarme
                updateButtons();
            }
        }.start();

        isRunning = true;
        updateButtons();
    }

    private void pauseTimer() {
        if (isRunning) {
            countDownTimer.cancel();
            isRunning = false;
            updateButtons();
        }
    }

    private void stopTimer() {
        countDownTimer.cancel();
        isRunning = false;
        timeLeftInMillis = 600000; // Resetar para 25 minutos
        updateTimerText();
        updateButtons();
    }

    private void updateTimerText() {
        int minutes = (int) (timeLeftInMillis / 1000) / 60;
        int seconds = (int) (timeLeftInMillis / 1000) % 60;
        String timeFormatted = String.format(Locale.getDefault(), "%02d:%02d", minutes, seconds);
        textViewTimer.setText(timeFormatted);
    }

    private void updateButtons() {
        if (isRunning) {
            buttonPlay.setEnabled(false);
            buttonPause.setEnabled(true);
            buttonStop.setEnabled(true);
        } else {
            buttonPlay.setEnabled(true);
            buttonPause.setEnabled(false);
            buttonStop.setEnabled(false);
        }
    }
}
