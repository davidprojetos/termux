package com.example.apifire.managers;

import android.content.Context;
import android.widget.EditText;
import android.widget.Toast;

public class LoginManager {
    private EditText editTextUsername, editTextPassword;
    private Context context;

    public LoginManager(EditText editTextUsername, EditText editTextPassword, Context context) {
        this.editTextUsername = editTextUsername;
        this.editTextPassword = editTextPassword;
        this.context = context;
    }

    public void performLogin() {
        String username = editTextUsername.getText().toString();
        String password = editTextPassword.getText().toString();
        if (username.equals("admin") && password.equals("1234")) {
            Toast.makeText(context, "Login Successful", Toast.LENGTH_SHORT).show();
        } else {
            Toast.makeText(context, "Invalid Credentials", Toast.LENGTH_SHORT).show();
        }
    }
}

