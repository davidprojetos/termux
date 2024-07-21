package com.example.apifire;

import android.os.AsyncTask;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;

import java.util.Properties;

import javax.mail.Message;
import javax.mail.MessagingException;
import javax.mail.PasswordAuthentication;
import javax.mail.Session;
import javax.mail.Transport;
import javax.mail.internet.InternetAddress;
import javax.mail.internet.MimeMessage;

public class ContactFragment extends Fragment {

    private EnvioEmail envioEmail;
    private EditText editTextRecipient, editTextName, editTextSubject, editTextMessage;
    private Button buttonSend;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View view = inflater.inflate(R.layout.fragment_contact, container, false);

        editTextRecipient = view.findViewById(R.id.editTextRecipient);
        editTextName = view.findViewById(R.id.editTextName);
        editTextSubject = view.findViewById(R.id.editTextSubject);
        editTextMessage = view.findViewById(R.id.editTextMessage);
        buttonSend = view.findViewById(R.id.buttonSend);
        envioEmail = new EnvioEmail(editTextRecipient, editTextName, editTextSubject, editTextMessage, buttonSend);
        
        return view;
    }

    
}
